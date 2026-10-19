import pkgutil
import sys
from importlib import import_module, reload
import pytest
from django.apps import apps
from django.contrib.auth.models import User
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder
from django.conf import settings

class TestMigrationLoader:
    
    @pytest.fixture(autouse=True)
    def setup(self, settings):
        # Add a dummy app to INSTALLED_APPS for testing
        settings.INSTALLED_APPS += ['my_test_app']

        # Create the MigrationLoader instance
        self.loader = MigrationLoader(connection=None, load=True, ignore_no_migrations=False)
    
    def test_load_disk_with_no_migrations(self, monkeypatch):
        # Simulate a case where there are no migrations module
        monkeypatch.setattr(self.loader, 'migrations_module', lambda x: (None, False))
        self.loader.load_disk()
        
        assert 'my_test_app' in self.loader.unmigrated_apps
        assert len(self.loader.disk_migrations) == 0

    def test_load_disk_with_empty_module(self, monkeypatch):
        # Simulate a case where migrations module exists but is empty
        monkeypatch.setattr(self.loader, 'migrations_module', lambda x: ('my_test_app.migrations', True))

        class EmptyMigrations:
            __path__ = []

        monkeypatch.setattr('importlib.import_module', lambda name: EmptyMigrations())
        self.loader.load_disk()

        assert 'my_test_app' in self.loader.unmigrated_apps
        assert len(self.loader.disk_migrations) == 0

    def test_load_disk_with_valid_migration(self, monkeypatch):
        # Simulate a case with a valid migration
        monkeypatch.setattr(self.loader, 'migrations_module', lambda x: ('my_test_app.migrations', True))

        class ValidMigrationModule:
            __path__ = ['my_test_app/migrations']
        
            class Migration:
                def __init__(self, name, app_label):
                    self.name = name
                    self.app_label = app_label

        monkeypatch.setattr('importlib.import_module', lambda name: ValidMigrationModule())
        monkeypatch.setattr(pkgutil, 'iter_modules', lambda path=None: [(None, '0001_initial', False)])
        
        self.loader.load_disk()

        assert 'my_test_app' in self.loader.migrated_apps
        assert ('my_test_app', '0001_initial') in self.loader.disk_migrations
        assert isinstance(self.loader.disk_migrations[('my_test_app', '0001_initial')], ValidMigrationModule.Migration)

    def test_load_disk_with_bad_migration(self, monkeypatch):
        # Simulate a case where the migration module has no Migration class
        monkeypatch.setattr(self.loader, 'migrations_module', lambda x: ('my_test_app.migrations', True))

        class BadMigrationModule:
            __path__ = ['my_test_app/migrations']

        monkeypatch.setattr('importlib.import_module', lambda name: BadMigrationModule())
        monkeypatch.setattr(pkgutil, 'iter_modules', lambda path=None: [(None, '0001_initial', False)])
        
        with pytest.raises(BadMigrationError):
            self.loader.load_disk()