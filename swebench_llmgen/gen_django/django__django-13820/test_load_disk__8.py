import pkgutil
import sys
from importlib import import_module, reload
from django.apps import apps
from django.contrib.auth.models import User
from django.db import migrations, models
import pytest

class MigrationLoader:
    def __init__(self, connection, load, ignore_no_migrations, replace_migrations):
        self.connection = connection
        self.load = load
        self.ignore_no_migrations = ignore_no_migrations
        self.replace_migrations = replace_migrations
        self.disk_migrations = {}
        self.unmigrated_apps = set()
        self.migrated_apps = set()

    def migrations_module(self, app_label):
        return ('myapp.migrations', True)

    def load_disk(self):
        """Load the migrations from all INSTALLED_APPS from disk."""
        self.disk_migrations = {}
        self.unmigrated_apps = set()
        self.migrated_apps = set()
        for app_config in apps.get_app_configs():
            module_name, explicit = self.migrations_module(app_config.label)
            if module_name is None:
                self.unmigrated_apps.add(app_config.label)
                continue
            was_loaded = module_name in sys.modules
            try:
                module = import_module(module_name)
            except ModuleNotFoundError as e:
                if (
                    (explicit and self.ignore_no_migrations) or
                    (not explicit and 'migrations' in e.name.split('.'))
                ):
                    self.unmigrated_apps.add(app_config.label)
                    continue
                raise
            else:
                if getattr(module, '__file__', None) is None or not hasattr(module, '__path__'):
                    self.unmigrated_apps.add(app_config.label)
                    continue
                if was_loaded:
                    reload(module)
            self.migrated_apps.add(app_config.label)
            migration_names = {
                name for _, name, is_pkg in pkgutil.iter_modules(module.__path__)
                if not is_pkg and name[0] not in '_~'
            }
            for migration_name in migration_names:
                migration_path = '%s.%s' % (module_name, migration_name)
                try:
                    migration_module = import_module(migration_path)
                except ImportError as e:
                    if 'bad magic number' in str(e):
                        raise ImportError("Couldn't import %r as it appears to be a stale "
                                          ".pyc file." % migration_path) from e
                    else:
                        raise
                if not hasattr(migration_module, "Migration"):
                    raise BadMigrationError(
                        "Migration %s in app %s has no Migration class" % (migration_name, app_config.label)
                    )
                self.disk_migrations[app_config.label, migration_name] = migration_module.Migration(
                    migration_name, app_config.label,
                )

def test_load_disk_with_migrations(settings):
    settings.INSTALLED_APPS += ['myapp']
    
    # Create a dummy migration for the app
    class Migration(migrations.Migration):
        dependencies = []
        operations = [
            migrations.CreateModel(
                name='TestUser',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('username', models.CharField(max_length=150)),
                ],
            ),
        ]

    sys.modules['myapp.migrations'] = type(sys)('migrations')
    sys.modules['myapp.migrations'].Migration = Migration

    loader = MigrationLoader(connection=None, load=True, ignore_no_migrations=False, replace_migrations={})
    loader.load_disk()

    assert 'myapp' in loader.migrated_apps
    assert ('myapp', '0001_initial') in loader.disk_migrations
    assert loader.disk_migrations[('myapp', '0001_initial')].operations[0].model == 'TestUser'