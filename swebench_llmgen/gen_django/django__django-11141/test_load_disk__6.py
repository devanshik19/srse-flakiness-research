import sys
import pkgutil
import pytest
from django.apps import AppConfig, apps
from django.contrib.auth.models import User
from django.db.migrations.loader import MigrationLoader
from django.db import migrations
from unittest.mock import MagicMock

class TestMigrationLoader:

    @pytest.fixture(autouse=True)
    def setup(self, settings):
        # Set up required settings for testing
        settings.INSTALLED_APPS = ['auth']  # Use default Django auth app for migration
        self.loader = MigrationLoader(None, None, ignore_no_migrations=False)

    def test_load_disk_no_migrations_module(self):
        app_config = MagicMock(spec=AppConfig)
        app_config.label = 'no_migrations_app'
        apps.all_models['no_migrations_app'] = {}

        loader = self.loader
        loader.migrations_module = MagicMock(return_value=(None, False))
        
        loader.load_disk()

        assert 'no_migrations_app' in loader.unmigrated_apps
        assert len(loader.disk_migrations) == 0

    def test_load_disk_empty_module(self):
        app_config = MagicMock(spec=AppConfig)
        app_config.label = 'empty_app'
        apps.all_models['empty_app'] = {}

        loader = self.loader
        loader.migrations_module = MagicMock(return_value=('empty_app.migrations', True))
        
        # Create an empty migrations module
        sys.modules['empty_app.migrations'] = MagicMock(__file__=None, __path__=[])

        loader.load_disk()

        assert 'empty_app' in loader.unmigrated_apps
        assert len(loader.disk_migrations) == 0

    def test_load_disk_invalid_migration_class(self):
        app_config = MagicMock(spec=AppConfig)
        app_config.label = 'invalid_migration_app'
        apps.all_models['invalid_migration_app'] = {}

        loader = self.loader
        loader.migrations_module = MagicMock(return_value=('invalid_migration_app.migrations', True))

        # Simulate a migrations directory with an invalid migration file
        migration_module = MagicMock()
        migration_module.Migration = None
        
        sys.modules['invalid_migration_app.migrations'] = MagicMock(__path__=[None])
        pkgutil.iter_modules = MagicMock(return_value=[('invalid_migration', False)])
        import_module = MagicMock(return_value=migration_module)

        with pytest.raises(BadMigrationError):
            loader.load_disk()

    def test_load_disk_success(self):
        app_config = MagicMock(spec=AppConfig)
        app_config.label = 'valid_migration_app'
        apps.all_models['valid_migration_app'] = {}

        loader = self.loader
        loader.migrations_module = MagicMock(return_value=('valid_migration_app.migrations', True))

        migration_module = MagicMock()
        class MockMigration:
            def __init__(self, name, app_label):
                self.name = name
                self.app_label = app_label
        migration_module.Migration = MockMigration
        
        sys.modules['valid_migration_app.migrations'] = MagicMock(__path__=[None])
        pkgutil.iter_modules = MagicMock(return_value=[('001_initial', False)])
        
        with pytest.patch('importlib.import_module', return_value=migration_module):
            loader.load_disk()

        assert 'valid_migration_app' in loader.migrated_apps
        assert len(loader.disk_migrations) == 1
        assert ('valid_migration_app', '001_initial') in loader.disk_migrations