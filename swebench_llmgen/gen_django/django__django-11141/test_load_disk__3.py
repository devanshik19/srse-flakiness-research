import pytest
from django.apps import apps
from django.contrib.auth.models import User
from django.db.migrations.loader import MigrationLoader
from django.db import connections

class TestMigrationLoader:
    
    @pytest.fixture
    def migration_loader(self):
        return MigrationLoader(connections['default'], load=True, ignore_no_migrations=True)

    def test_load_disk_no_migrations(self, migration_loader):
        apps.get_app_configs = lambda: [User._meta.app_config]  # only default auth app
        migration_loader.load_disk()
        assert migration_loader.unmigrated_apps == {'auth'}
        assert migration_loader.disk_migrations == {}

    def test_load_disk_with_migrations(self, migration_loader):
        apps.get_app_configs = lambda: [User._meta.app_config]
        
        # Assume 'auth' app has migrations 
        migration_loader.migrations_module = lambda label: ('django.contrib.auth.migrations', False)
        migration_loader.load_disk()

        assert 'auth' in migration_loader.migrated_apps
        assert len(migration_loader.disk_migrations) > 0  # expect migrations to be loaded

    def test_load_disk_handle_importerror(self, migration_loader):
        apps.get_app_configs = lambda: [User._meta.app_config]
        
        # Simulate that the migrations module cannot be imported
        migration_loader.migrations_module = lambda label: ('non_existent_migrations', True)

        migration_loader.load_disk()
        assert 'auth' in migration_loader.unmigrated_apps

    def test_load_disk_stale_pyc_file(self, migration_loader):
        apps.get_app_configs = lambda: [User._meta.app_config]

        migration_loader.migrations_module = lambda label: ('django.contrib.auth.migrations', False)
        
        with pytest.raises(ImportError, match='stale'):
            migration_loader.load_disk()