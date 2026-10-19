import pkgutil
import sys
from importlib import import_module, reload
from django.apps import apps
from django.db import models
from django.contrib.auth.models import User
from django.db.migrations.loader import MigrationLoader
import pytest
from unittest.mock import patch

@pytest.fixture
def migration_loader():
    return MigrationLoader(connection=None, load=True, ignore_no_migrations=False, replace_migrations={})

def test_load_disk_with_no_migrations(migration_loader):
    with patch('django.apps.apps.get_app_configs', return_value=[]):
        migration_loader.load_disk()
        assert migration_loader.disk_migrations == {}
        assert migration_loader.unmigrated_apps == set()
        assert migration_loader.migrated_apps == set()

def test_load_disk_with_valid_migrations(migration_loader):
    app_label = 'auth'
    module_name = 'django.contrib.auth.migrations'
    
    # Assuming the "auth" app has migrations
    with patch('django.apps.apps.get_app_configs', return_value=[User._meta.app_config]):
        with patch('django.db.migrations.loader.import_module', side_effect=lambda name: import_module(name)):
            migration_loader.load_disk()
        
        assert (app_label, '0001_initial') in migration_loader.disk_migrations
        assert migration_loader.unmigrated_apps == set()
        assert migration_loader.migrated_apps == {app_label}

def test_load_disk_with_missing_migrations(migration_loader):
    app_label = 'missing_app'
    
    with patch('django.apps.apps.get_app_configs', return_value=[models.get_app_config(app_label)]):
        with patch('django.db.migrations.loader.import_module', side_effect=ModuleNotFoundError):
            migration_loader.load_disk()

        assert migration_loader.unmigrated_apps == {app_label}
        assert migration_loader.migrated_apps == set()

def test_load_disk_with_stale_pyc_file(migration_loader):
    app_label = 'auth'
    migration_name = '0001_initial'
    
    class FakeModule:
        __path__ = []
        Migration = None
    
    with patch('django.apps.apps.get_app_configs', return_value=[User._meta.app_config]):
        with patch('django.db.migrations.loader.import_module', side_effect=lambda name: FakeModule() if name == f'django.contrib.auth.migrations.{migration_name}' else ModuleNotFoundError):
            with pytest.raises(BadMigrationError):
                migration_loader.load_disk()