import pytest
import pkgutil
import sys
from django.apps import apps
from django.contrib.auth.models import User
from django.db import migrations
from django.utils.module_loading import import_string
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.exceptions import BadMigrationError

def create_migration(app_label, name):
    migrations_dir = f"{app_label}/migrations"
    migration_file = f"{migrations_dir}/{name}.py"
    with open(migration_file, 'w') as f:
        f.write(f"""
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = []
    operations = []
""")

@pytest.fixture
def set_up_migrations():
    app_label = 'auth'
    migration_name = '0001_initial'
    create_migration(app_label, migration_name)
    yield
    # Clean up migration file after test
    migration_file = f"{app_label}/migrations/{migration_name}.py"
    try:
        os.remove(migration_file)
    except OSError:
        pass

def test_load_disk_with_valid_migrations(set_up_migrations):
    connection = None  # Assuming the connection is managed by pytest-django
    loader = MigrationLoader(connection, load=True, ignore_no_migrations=False, replace_migrations=None)

    loader.load_disk()

    assert (loader.disk_migrations[('auth', '0001_initial')] is not None)
    assert 'auth' in loader.migrated_apps
    assert 'django.contrib.auth' not in loader.unmigrated_apps

def test_load_disk_with_no_migrations():
    app_label = 'no_migrations_app'
    apps.app_configs[app_label] = apps.get_app_config('auth')  # Using a dummy app config

    loader = MigrationLoader(None, load=True, ignore_no_migrations=False, replace_migrations=None)
    loader.load_disk()

    assert len(loader.disk_migrations) == 0
    assert app_label in loader.unmigrated_apps

def test_load_disk_handles_bad_migration():
    app_label = 'bad_migration_app'
    migrations_dir = f"{app_label}/migrations"
    os.makedirs(migrations_dir, exist_ok=True)
    with open(f"{migrations_dir}/bad_migration.py", 'w') as f:
        f.write("not a migration class")

    loader = MigrationLoader(None, load=True, ignore_no_migrations=False, replace_migrations=None)

    with pytest.raises(BadMigrationError):
        loader.load_disk()