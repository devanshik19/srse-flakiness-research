import pkgutil
import sys
from importlib import import_module, reload
from django.apps import apps
from django.contrib.auth.models import User
from django.db import migrations
from django.db.migrations.loader import MigrationLoader
import pytest

@pytest.fixture
def migration_loader():
    return MigrationLoader(None, load=False, ignore_no_migrations=True, replace_migrations={})

def test_load_disk_no_migrations(migration_loader):
    migration_loader.load_disk()
    assert migration_loader.disk_migrations == {}
    assert migration_loader.unmigrated_apps == {app.label for app in apps.get_app_configs()}
    assert migration_loader.migrated_apps == set()

def test_load_disk_with_valid_migrations(migration_loader):
    # Create a dummy migration for the 'auth' app
    auth_app = apps.get_app_config('auth')
    migration_module_name = 'django.contrib.auth.migrations'
    module = import_module(migration_module_name)
    
    migration_name = '0001_initial'
    migration_loader.disk_migrations[(auth_app.label, migration_name)] = migrations.RunPython(lambda apps, schema_editor: None)
    
    # Reload the module with mock migrations
    migration_loader.migrations_module = lambda label: (migration_module_name, True)
    migration_loader.migrated_apps.add(auth_app.label)
    
    # Mock the app config to simulate installed apps
    def mock_get_app_configs():
        return [auth_app]
    
    apps.get_app_configs = mock_get_app_configs
    migration_loader.load_disk()
    
    assert (auth_app.label, migration_name) in migration_loader.disk_migrations
    assert migration_loader.unmigrated_apps == set()
    assert migration_loader.migrated_apps == {auth_app.label}

def test_load_disk_invalid_migration_class(migration_loader):
    # Create a dummy migration for the 'auth' app with a missing Migration class
    auth_app = apps.get_app_config('auth')
    
    migration_module_name = 'django.contrib.auth.migrations'
    migration_name = 'invalid_migration'

    # Simulating the migration module without Migration class
    class InvalidMigrationModule:
        pass

    sys.modules[migration_module_name + '.' + migration_name] = InvalidMigrationModule()
    
    # Mock the app config to simulate installed apps
    def mock_get_app_configs():
        return [auth_app]
    
    apps.get_app_configs = mock_get_app_configs
    with pytest.raises(migrations.BadMigrationError):
        migration_loader.load_disk()

    assert migration_loader.unmigrated_apps == set()
    assert migration_loader.migrated_apps == {auth_app.label}