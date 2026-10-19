import pytest
from django.apps import AppConfig
from django.contrib.auth.models import User
from django.db import migrations
from django.db.migrations.loader import MigrationLoader


class TestMigrationLoader:
    @pytest.fixture(autouse=True)
    def setup(self, settings):
        settings.INSTALLED_APPS = [
            'django.contrib.auth',
            'myapp',  # This should be replaced with actual test app name
        ]
        # Here you can create a test app or migrate it
        # For example's sake, we're assuming `myapp` is your test app which is already set up

    def test_load_disk(self):
        loader = MigrationLoader(connection=None, load=True, ignore_no_migrations=False, replace_migrations=None)

        # Simulate adding migrations to the app
        app_config = AppConfig.create('myapp', 'myapp')
        loader.migrations_module(app_config.label)  # Replace with actual migration path as necessary

        # Assuming that 'myapp/migrations/0001_initial.py' is a valid migration
        loader.load_disk()

        # Check if known migration is present
        assert ('myapp', '0001_initial') in loader.disk_migrations
        assert loader.migrated_apps == {'myapp'}
        
        # Check unmanaged apps
        assert loader.unmigrated_apps == set()

    def test_load_disk_handles_no_migrations(self, settings):
        settings.INSTALLED_APPS = ['django.contrib.auth', 'app_without_migrations']  # Replace for test
        
        loader = MigrationLoader(connection=None, load=True, ignore_no_migrations=True, replace_migrations=None)
        loader.load_disk()

        assert ('app_without_migrations', None) not in loader.disk_migrations
        assert 'app_without_migrations' in loader.unmigrated_apps

    def test_load_disk_raises_on_bad_migration(self):
        loader = MigrationLoader(connection=None, load=True, ignore_no_migrations=False, replace_migrations=None)

        # Add a corrupt migration file
        app_config = AppConfig.create('myapp', 'myapp')
        loader.migrations_module(app_config.label)

        with pytest.raises(BadMigrationError):
            loader.load_disk()