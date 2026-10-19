import pytest
from django.apps import AppConfig
from django.contrib.auth.models import User
from django.db import migrations
from django.db.migrations.loader import MigrationLoader
from unittest.mock import patch, MagicMock

# Create a mock app config for the tests
class MockAppConfig(AppConfig):
    name = 'mock_app'
    label = 'mock_app'

@pytest.fixture
def mock_app_config():
    return MockAppConfig()

@pytest.fixture
def migration_loader():
    return MigrationLoader(None, load=True, ignore_no_migrations=True)

def test_load_disk_no_migrations(migration_loader, mock_app_config):
    with patch('django.apps.apps.get_app_configs', return_value=[mock_app_config]):
        migration_loader.load_disk()
        assert mock_app_config.label in migration_loader.unmigrated_apps
        assert not migration_loader.migrated_apps
        assert not migration_loader.disk_migrations

def test_load_disk_with_migrations(migration_loader, mock_app_config):
    mock_module = MagicMock()
    mock_module.__file__ = 'mock_file.py'
    mock_module.__path__ = ['']
    migration_name = '0001_initial'
    
    with patch('django.apps.apps.get_app_configs', return_value=[mock_app_config]), \
         patch('django.db.migrations.loader.import_module', return_value=mock_module), \
         patch('pkgutil.iter_modules', return_value=[(None, migration_name, False)]), \
         patch('django.db.migrations.loader.import_module', side_effect=[MagicMock(spec=migrations), 
                                                                        ImportError("bad magic number"), 
                                                                        MagicMock(spec=migrations)]):
        
        mock_migration = MagicMock()
        mock_migration.Migration.return_value = MagicMock()
        migration_loader.load_disk()
        
        assert mock_app_config.label in migration_loader.migrated_apps
        assert (mock_app_config.label, migration_name) in migration_loader.disk_migrations
        assert isinstance(migration_loader.disk_migrations[(mock_app_config.label, migration_name)], migrations.Migration)

def test_load_disk_importerror_handling(migration_loader, mock_app_config):
    with patch('django.apps.apps.get_app_configs', return_value=[mock_app_config]), \
         patch('django.db.migrations.loader.import_module', side_effect=ImportError("No module named 'mock_app.migrations'")):
         
        migration_loader.load_disk()
        assert mock_app_config.label in migration_loader.unmigrated_apps
        assert not migration_loader.migrated_apps
        assert not migration_loader.disk_migrations

def test_load_disk_bad_migration(migration_loader, mock_app_config):
    mock_module = MagicMock()
    mock_module.__file__ = 'mock_file.py'
    mock_module.__path__ = ['']
    
    with patch('django.apps.apps.get_app_configs', return_value=[mock_app_config]), \
         patch('django.db.migrations.loader.import_module', return_value=mock_module), \
         patch('pkgutil.iter_modules', return_value=[(None, '0001_initial', False)]), \
         patch('django.db.migrations.loader.import_module', side_effect=BadMigrationError("Bad migration")):

        with pytest.raises(BadMigrationError):
            migration_loader.load_disk()