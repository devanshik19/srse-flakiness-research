import pkgutil
import sys
from importlib import import_module, reload
from django.apps import apps
from django.conf import settings
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder
from django.contrib.auth.models import User

def test_load_disk(migration_loader):
    # Setup the test data for migrations
    app_label = 'auth'
    migration_name = '0001_initial'

    # Create the application by simulating it is installed
    apps.get_app_config(app_label)

    # Create migration module dynamically
    migration_module_code = f"""
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = []
    operations = []
"""
    module_name = f"{app_label}.migrations.{migration_name}"
    migration_module = import_module(module_name)

    # Create an empty module for migrations (for testing)
    if migration_module:
        sys.modules[module_name] = migration_module

    # Initialize the MigrationLoader
    connection = MigrationRecorder(connection=None)
    loader = MigrationLoader(connection, load=True, ignore_no_migrations=False, replace_migrations={})

    # Load the disk migrations
    loader.load_disk()

    # Assert the loaded migrations
    assert (app_label, migration_name) in loader.disk_migrations
    assert app_label in loader.migrated_apps
    assert app_label not in loader.unmigrated_apps

    # Cleanup: reset sys.modules to remove the dynamically added module
    del sys.modules[module_name]

def test_load_disk_no_migrations(migration_loader):
    # Test case where no migrations are found
    app_label = 'auth'

    # Make sure the migration directory is added
    apps.get_app_config(app_label)

    # Initialize the MigrationLoader
    connection = MigrationRecorder(connection=None)
    loader = MigrationLoader(connection, load=True, ignore_no_migrations=False, replace_migrations={})

    # Simulate the absence of migrations
    loader.migrations_module = lambda label: (None, False)
    loader.load_disk()

    # Assert that there are no migrated apps and the app is in unmigrated apps
    assert app_label in loader.unmigrated_apps
    assert app_label not in loader.migrated_apps