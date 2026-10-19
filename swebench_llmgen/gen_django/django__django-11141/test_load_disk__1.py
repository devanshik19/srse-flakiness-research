import sys
import pkgutil
from importlib import import_module, reload
import pytest
from django.apps import apps
from django.conf import settings
from django.db.migrations.loader import MigrationLoader
from django.contrib.auth.models import User
from django.core.management import call_command

class MockAppConfig:
    def __init__(self, label):
        self.label = label

def setup_migrations():
    # Create a mock migration module in memory
    migration_code = """
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = []
    operations = []
"""
    module_name = 'mockapp.migrations'
    sys.modules[module_name] = import_module(module_name)

    # Create a mock 'migrations' package
    pkgutil.get_data.return_value = migration_code.encode('utf-8')

def test_load_disk_with_migrations(monkeypatch):
    # Set up mock app config
    mock_app_config = MockAppConfig('mockapp')
    
    # Replace the actual app configs with our mock
    monkeypatch.setattr(apps, 'get_app_configs', lambda: [mock_app_config])
    
    # Create instance of MigrationLoader
    loader = MigrationLoader(None, True, False)
    
    # Set up mock migrations
    setup_migrations()

    # Run load_disk
    loader.load_disk()

    # Verify the migrations were loaded
    assert ('mockapp', '0001_initial') in loader.disk_migrations
    assert mock_app_config.label in loader.migrated_apps
    assert not loader.unmigrated_apps

def test_load_disk_no_migrations(monkeypatch):
    # Set up mock app config with no migrations
    mock_app_config = MockAppConfig('emptyapp')

    # Replace the actual app configs with our mock
    monkeypatch.setattr(apps, 'get_app_configs', lambda: [mock_app_config])

    # Create instance of MigrationLoader
    loader = MigrationLoader(None, True, False)

    # Run load_disk
    loader.load_disk()

    # Verify no migrations were loaded
    assert not loader.disk_migrations
    assert mock_app_config.label in loader.unmigrated_apps
    assert not loader.migrated_apps