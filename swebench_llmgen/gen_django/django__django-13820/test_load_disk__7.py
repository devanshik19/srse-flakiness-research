import pytest
from django.contrib.auth.models import User
from django.apps import apps
from django.db import migrations
from django.db.migrations.loader import MigrationLoader

def test_load_disk(monkeypatch):
    # Create a mock app config with migrations
    class MockAppConfig:
        label = 'mock_app'
        
    mock_migration_module = """
from django.db import migrations

class Migration(migrations.Migration):
    initial = True

    operations = [
        migrations.CreateModel(
            name='MockModel',
            fields=[
                ('id', migrations.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
"""

    # Mock the migrations_module method to return the mock module
    def mock_migrations_module(app_label):
        return ('mock_app.migrations', True)

    monkeypatch.setattr(MigrationLoader, 'migrations_module', mock_migrations_module)

    # Add a mock migration module to sys.modules
    import sys
    sys.modules['mock_app.migrations'] = type(sys)('mock_app.migrations')
    exec(mock_migration_module, sys.modules['mock_app.migrations'].__dict__)

    # Prepare MigrationLoader instance
    loader = MigrationLoader(None, None, False, None)

    # Run the load_disk method
    loader.load_disk()

    # Verify the correct migrations are loaded
    assert ('mock_app', '0001_initial') in loader.disk_migrations
    assert loader.migrated_apps == {'mock_app'}
    assert loader.unmigrated_apps == set()

    # Mock a case where the migration module does not exist
    def mock_migrations_module_invalid(app_label):
        return (None, False)
    
    monkeypatch.setattr(MigrationLoader, 'migrations_module', mock_migrations_module_invalid)
    loader.load_disk()

    # Verify that the unmigrated_apps list is updated
    assert 'mock_app' in loader.unmigrated_apps