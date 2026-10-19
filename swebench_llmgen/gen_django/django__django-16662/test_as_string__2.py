import pytest
import re
from django.db import migrations
from django.db.migrations.writer import MigrationWriter
from django.contrib.auth.models import User

# Test class to simulate a migration
class FakeMigration:
    def __init__(self):
        self.operations = []
        self.dependencies = []
        self.replaces = None
        self.initial = False

# Test function for MigrationWriter.as_string
def test_as_string():
    # Create a FakeMigration object
    migration = FakeMigration()

    # Instantiate MigrationWriter
    writer = MigrationWriter(migration, include_header=True)

    # Test for the header inclusion
    result = writer.as_string()
    assert "version" in result
    assert "timestamp" in result

    # Test when there are no operations
    assert "operations" not in result

    # Add a simulated operation
    migration.operations = [migrations.RunPython(lambda apps, schema_editor: None)]
    result = writer.as_string()

    # Test for operations being present
    assert "operations" in result

    # Test dependencies
    migration.dependencies = [("app_name", "MigrationName")]
    result = writer.as_string()
    assert "dependencies" in result
    assert re.search(r'^\s*app_name\.MigrationName,\s*$', result, re.MULTILINE)

    # Test replaces
    migration.replaces = ("app_name", "OldMigration")
    result = writer.as_string()
    assert "replaces =" in result
    assert "OldMigration" in result

    # Test initial
    migration.initial = True
    result = writer.as_string()
    assert "initial = True" in result