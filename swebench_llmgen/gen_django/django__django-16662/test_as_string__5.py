import pytest
from django.db import migrations
from django.contrib.auth.models import User
from django.utils.timezone import now
from django import get_version

# Assuming the MigrationWriter class is correctly imported
from django.db.migrations.writer import MigrationWriter

class MockOperation:
    def __init__(self, name):
        self.name = name

class MockMigration:
    def __init__(self, operations, dependencies, replaces=None, initial=False):
        self.operations = operations
        self.dependencies = dependencies
        self.replaces = replaces
        self.initial = initial

def test_as_string():
    # Arrange
    operations = [MockOperation('CreateUser'), MockOperation('AddEmailField')]
    dependencies = [('app_name', '0001_initial')]
    migration = MockMigration(operations, dependencies, initial=True)
    writer = MigrationWriter(migration, include_header=True)

    # Act
    result = writer.as_string()

    # Assert
    assert "initial = True" in result
    assert "replaces = None" in result  # Assuming replaces is not set
    assert "from django.db import migrations" in result
    assert "    dependencies = [" in result
    assert "        ('app_name', '0001_initial')," in result
    assert "operations = [" in result
    assert "CreateUser" in result
    assert "AddEmailField" in result
    assert f"# {get_version()}" in result  # Check for version in header
    assert "timestamp" in result  # Check for timestamp in header