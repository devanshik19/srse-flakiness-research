import pkgutil
import sys
from importlib import import_module, reload
from django.apps import apps
from django.conf import settings
from django.db import migrations
from django.db.migrations.loader import MigrationLoader
from django.contrib.auth.models import User
import pytest

@pytest.fixture
def migration_loader():
    return MigrationLoader(None, True, False)

def test_load_disk_with_no_apps(migration_loader):
    # Clear all apps
    apps.clear_cache()
    migration_loader.load_disk()
    assert migration_loader.disk_migrations == {}
    assert migration_loader.unmigrated_apps == set()
    assert migration_loader.migrated_apps == set()

def test_load_disk_with_unmigrated_apps(migration_loader):
    class DummyAppConfig:
        label = 'dummy_app'

    apps.get_app_configs = lambda: [DummyAppConfig()]
    
    migration_loader.load_disk()
    assert 'dummy_app' in migration_loader.unmigrated_apps
    assert migration_loader.disk_migrations == {}
    assert migration_loader.migrated_apps == set()

def test_load_disk_with_migration_import_error(migration_loader):
    class DummyAppConfig:
        label = 'dummy_app'

    def mock_migrations_module(app_label):
        return (None, False)

    migration_loader.migrations_module = mock_migrations_module
    apps.get_app_configs = lambda: [DummyAppConfig()]

    migration_loader.load_disk()
    assert 'dummy_app' in migration_loader.unmigrated_apps
    assert migration_loader.disk_migrations == {}
    assert migration_loader.migrated_apps == set()

def test_load_disk_with_valid_migrations(migration_loader):
    class DummyMigration:
        class Migration:
            def __init__(self, name, app_label):
                self.name = name
                self.app_label = app_label

    class DummyAppConfig:
        label = 'dummy_app'

    def mock_migrations_module(app_label):
        return ('dummy_app.migrations', True)

    def mock_import_module(module_name):
        if module_name == 'dummy_app.migrations':
            return DummyMigration
        raise ImportError("Module not found")

    migration_loader.migrations_module = mock_migrations_module
    migration_loader.import_module = mock_import_module
    apps.get_app_configs = lambda: [DummyAppConfig()]

    migration_loader.load_disk()
    assert ('dummy_app', 'dummy_migration') in migration_loader.disk_migrations
    assert 'dummy_app' in migration_loader.migrated_apps
    assert migration_loader.unmigrated_apps == set()