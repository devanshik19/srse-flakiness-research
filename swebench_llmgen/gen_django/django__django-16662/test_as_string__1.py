import pytest
from django.db import migrations
from django.contrib.auth.models import User
from your_module_path import MigrationWriter  # Replace `your_module_path` with the correct import path

@pytest.fixture
def migration():
    """Fixture to provide a sample migration object for testing."""
    return migrations.Migration(
        name='TestMigration',
        app_label='your_app_label',  # Replace with actual app label
        operations=[],
        dependencies=[],
        replaces=None,
        initial=False,
    )

def test_as_string_no_operations(migration):
    writer = MigrationWriter(migration=migration, include_header=False)
    result = writer.as_string()
    assert "operations" not in result
    assert "dependencies" not in result

def test_as_string_with_operations(migration):
    # Create a dummy operation for testing
    operation = migrations.CreateModel(
        name='TestModel',
        fields=[
            ('id', migrations.AutoField(auto_created=True, primary_key=True, serialize=False)),
            ('username', models.CharField(max_length=150, unique=True)),
        ],
    )
    migration.operations.append(operation)
    
    writer = MigrationWriter(migration=migration, include_header=False)
    result = writer.as_string()
    
    assert "CreateModel" in result
    assert "operations" in result
    assert "dependencies" not in result  # Still no dependencies

def test_as_string_with_dependencies(migration):
    migration.dependencies.append(('your_app_label', '0001_initial'))  # Replace with your actual app and migration name
    writer = MigrationWriter(migration=migration, include_header=False)
    result = writer.as_string()

    assert "dependencies" in result
    assert "your_app_label" in result  # Check that dependency appears in output

def test_as_string_with_replaces(migration):
    migration.replaces = [('your_app_label', '0001_initial')]  # Replace with your actual app and migration name
    writer = MigrationWriter(migration=migration, include_header=False)
    result = writer.as_string()

    assert "replaces" in result
    assert "your_app_label" in result  # Check that replaces appears in output

def test_as_string_with_header(migration):
    writer = MigrationWriter(migration=migration, include_header=True)
    result = writer.as_string()
    
    assert "version" in result  # Check that version from get_version() is included
    assert "timestamp" in result  # Check that the timestamp is included