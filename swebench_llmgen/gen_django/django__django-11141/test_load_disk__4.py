import sys
import pkgutil
import pytest
from importlib import import_module
from django.apps import apps
from django.contrib.auth.models import User
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder
from .exceptions import BadMigrationError

# Create a test app with migration modules
class TestMigrationLoader:
    @pytest.fixture(autouse=True)
    def setup_app(self, django_db_setup):
        # This will simulate an app with migrations
        self.test_app_label = "test_app"
        self.test_app_module_name = f"{self.test_app_label}.migrations"
        
        # Create a dummy migrations module
        sys.modules[self.test_app_module_name] = type(sys)(
            self.test_app_module_name)
        
        sys.modules[self.test_app_module_name].__path__ = [""]
        sys.modules[self.test_app_module_name].Migration = lambda *args: "Migration Object"
        
        apps.get_app_configs.cache_clear()  # Clear cache to ensure the app config is fresh
    
    def test_load_disk_with_valid_migrations(self):
        # Register the test app
        apps.get_app_configs.cache_clear()
        apps.get_app_configs = lambda: [User._meta.app_config] + [self.test_app_module_name]

        # Create the MigrationLoader instance
        migration_loader = MigrationLoader(None, None, ignore_no_migrations=True)
        
        # Load disk migrations
        migration_loader.load_disk()

        # Assert disk migrations are populated
        assert (self.test_app_label, "Migration") in migration_loader.disk_migrations

    def test_load_disk_with_no_migrations(self):
        # Simulate the absence of migration module
        del sys.modules[self.test_app_module_name]
        
        # Register the test app without migrations
        apps.get_app_configs.cache_clear()
        apps.get_app_configs = lambda: [User._meta.app_config] + [self.test_app_label]
        
        # Create the MigrationLoader instance
        migration_loader = MigrationLoader(None, None, ignore_no_migrations=True)

        # Load disk migrations
        migration_loader.load_disk()

        # Assert unmigrated apps are recorded
        assert self.test_app_label in migration_loader.unmigrated_apps

    def test_load_disk_with_bad_migration(self):
        bad_app_label = "bad_app"
        bad_app_module_name = f"{bad_app_label}.migrations"
        
        # Create a bad migration module
        sys.modules[bad_app_module_name] = type(sys)(bad_app_module_name)
        sys.modules[bad_app_module_name].__path__ = [""]
        
        # Simulate a migration without a Migration class
        apps.get_app_configs.cache_clear()
        apps.get_app_configs = lambda: [User._meta.app_config] + [bad_app_label]
        
        # Create the MigrationLoader instance
        migration_loader = MigrationLoader(None, None, ignore_no_migrations=False)
        
        # Load disk migrations and expect BadMigrationError
        with pytest.raises(BadMigrationError):
            migration_loader.load_disk()