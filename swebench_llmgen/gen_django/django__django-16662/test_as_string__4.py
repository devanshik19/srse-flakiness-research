import pytest
from django.db import migrations
from django.contrib.auth.models import User
from django.utils.timezone import now
from django import get_version
from your_module_path import MigrationWriter  # Replace with the actual module path

@pytest.fixture
def migration():
    return migrations.Migration("test_migration", "app_label", operations=[], dependencies=[])

def test_as_string_no_operations(migration):
    writer = MigrationWriter(migration, include_header=False)
    result = writer.as_string()
    
    assert "migrations." in result
    assert "operations" not in result
    assert "dependencies" not in result

def test_as_string_with_operations(migration):
    class DummyOperation:
        def serialize(self):
            return ("DummyOperation()", ["dummy_import"])

    migration.operations = [DummyOperation()]
    writer = MigrationWriter(migration, include_header=False)
    result = writer.as_string()
    
    assert "DummyOperation()" in result
    assert "dummy_import" in result

def test_as_string_with_dependencies(migration):
    migration.dependencies = [("app_label", "0001_initial")]
    writer = MigrationWriter(migration, include_header=False)
    result = writer.as_string()
    
    assert "app_label" in result

def test_as_string_initial(migration):
    migration.initial = True
    writer = MigrationWriter(migration, include_header=False)
    result = writer.as_string()
    
    assert "initial = True" in result

def test_as_string_replaces(migration):
    migration.replaces = [("app_label", "0002_auto")]
    writer = MigrationWriter(migration, include_header=False)
    result = writer.as_string()
    
    assert "replaces = " in result