import pytest
import pkgutil
import sys
from importlib import import_module, reload
from django.apps import apps
from django.contrib.auth.models import User
from django.db import migrations
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder
from .exceptions import BadMigrationError

@pytest.fixture
def migration_loader(settings):
    settings.INSTALLED_APPS = ['django.contrib.auth', 'myapp']
    return MigrationLoader(None, load=True, ignore_no_migrations=False, replace_migrations=None)

def test_load_disk_with_migrations(migration_loader):
    # Set up a mock migration module dynamically
    migrations_module = migrations.__name__ + '.myapp.migrations'
    module_name, _ = migration_loader.migrations_module('myapp')
    
    # Create a mock migration class
    class Migration:
        def __init__(self, name, app_label):
            self.name = name
            self.app_label = app_label
    
    # Simulate the presence of migration files
    sys.modules["myapp.migrations"] = pkgutil.new_module(migrations_module)
    sys.modules["myapp.migrations"].__path__ = []
    setattr(sys.modules["myapp.migrations"], 'Migration', Migration)
    
    # Call load_disk to load the migrations
    migration_loader.load_disk()
    
    # Check if migrations were loaded correctly
    assert migration_loader.migrated_apps == {'myapp'}
    assert (('myapp', 'my_migration') in migration_loader.disk_migrations)

def test_load_disk_no_migrations(migration_loader):
    # Simulate no migrations available for an app
    migration_loader.unmigrated_apps.add('myapp')
    
    migration_loader.load_disk()
    
    assert migration_loader.unmigrated_apps == {'myapp'}
    assert not migration_loader.migrated_apps

def test_load_disk_bad_migration_class(migration_loader):
    # Set up a mock migration with a bad class
    migrations_module = migrations.__name__ + '.myapp.migrations'
    module_name, _ = migration_loader.migrations_module('myapp')
    
    sys.modules["myapp.migrations"] = pkgutil.new_module(migrations_module)
    sys.modules["myapp.migrations"].__path__ = []
    # Creating an invalid migration class (missing Migration attribute)
    setattr(sys.modules["myapp.migrations"], 'BadMigration', object)
    
    with pytest.raises(BadMigrationError):
        migration_loader.load_disk()