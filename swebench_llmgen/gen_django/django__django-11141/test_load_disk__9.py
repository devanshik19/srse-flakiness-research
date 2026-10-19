import pytest
from django.apps import AppConfig
from django.contrib.auth.models import User
from django.db import migrations
from django.db.migrations.loader import MigrationLoader
from unittest.mock import MagicMock, patch


class TestMigrationLoader:
    
    @pytest.fixture(autouse=True)
    def setup_app_configs(self):
        # Simulate an app configuration with migrations
        class TestAppConfig(AppConfig):
            name = 'test_app'
            label = 'test_app'
        
        self.app_config = TestAppConfig()
        apps = MagicMock()
        apps.get_app_configs.return_value = [self.app_config]

        # Patch the apps module to provide the mocked version
        with patch('django.apps.apps', apps):
            yield

    @pytest.fixture
    def loader(self):
        # Initialize the MigrationLoader
        return MigrationLoader(connection=None, load=False, ignore_no_migrations=True)

    @patch('importlib.import_module')
    @patch('django.db.migrations.loader.pkgutil.iter_modules')
    def test_load_disk_with_migrations(self, mock_iter_modules, mock_import_module, loader):
        # Setup mocks
        mock_iter_modules.return_value = [(None, '0001_initial', False)]
        mock_import_module.return_value = MagicMock(__path__=[None], Migration=MagicMock())

        loader.load_disk()

        assert ('test_app', '0001_initial') in loader.disk_migrations
        assert 'test_app' in loader.migrated_apps
        assert not loader.unmigrated_apps

    @patch('importlib.import_module')
    @patch('django.db.migrations.loader.pkgutil.iter_modules')
    def test_load_disk_without_migrations(self, mock_iter_modules, mock_import_module, loader):
        # Simulate the case where the migrations module cannot be found
        mock_iter_modules.return_value = []
        mock_import_module.side_effect = ImportError("No module named 'test_app.migrations'")

        loader.load_disk()

        assert not loader.disk_migrations
        assert 'test_app' in loader.unmigrated_apps

    @patch('importlib.import_module')
    def test_load_disk_with_bad_migration(self, mock_import_module, loader):
        mock_import_module.side_effect = ImportError("bad magic number in 'test_app.migrations.0001_initial'")

        with pytest.raises(ImportError, match="Couldn't import"):
            loader.load_disk()

    @patch('importlib.import_module')
    @patch('django.db.migrations.loader.pkgutil.iter_modules')
    def test_load_disk_with_no_migration_class(self, mock_iter_modules, mock_import_module, loader):
        mock_iter_modules.return_value = [(None, '0001_initial', False)]
        mock_import_module.return_value = MagicMock(__path__=[None])
        mock_import_module.return_value.Migration = None

        with pytest.raises(BadMigrationError, match="Migration 0001_initial in app test_app has no Migration class"):
            loader.load_disk()