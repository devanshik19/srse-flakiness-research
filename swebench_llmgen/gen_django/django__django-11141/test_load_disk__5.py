import sys
import pkgutil
from importlib import import_module, reload
import pytest
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.db.migrations.exceptions import BadMigrationError
from django.db.migrations.loader import MigrationLoader

# Create a test module for migrations
class TestMigration:
    class Migration:
        def __init__(self, name, app_label):
            self.name = name
            self.app_label = app_label

def test_load_disk(mocker):
    # Mocking apps.get_app_configs to simulate installed apps
    mock_app_config = mocker.patch('django.apps.apps.get_app_configs', return_value=[
        mocker.Mock(label='app1'),
        mocker.Mock(label='app2'),
    ])
    mocker.patch('importlib.import_module', side_effect=[
        TestMigration,  # For app1
        ImportError("No module named 'migrations'"),  # For app2
    ])

    loader = MigrationLoader(None, load=False, ignore_no_migrations=True)

    # Call the method under test
    loader.load_disk()

    # Check migration loading
    assert ('app1', 'Migration') in loader.disk_migrations
    assert 'app1' in loader.migrated_apps
    assert 'app2' in loader.unmigrated_apps

    # Check for exception on migration without a Migration class
    with pytest.raises(BadMigrationError):
        loader.disk_migrations[('app1', 'Migration')] = None

    # Finally, ensure sys.modules state is correct for cleanup (if required)
    assert 'app1.migrations' in sys.modules
    assert 'app2.migrations' not in sys.modules