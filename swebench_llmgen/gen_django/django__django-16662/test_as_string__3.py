import pytest
from django.db import migrations
from django.contrib.auth.models import User
from django.utils.timezone import now
from django import get_version
from django.db.migrations.writer import MigrationWriter

@pytest.fixture
def mock_migration():
    migration = migrations.Migration("TestMigration", "test_app")
    migration.operations = []
    migration.dependencies = []
    migration.replaces = None
    migration.initial = False
    return migration

def test_as_string_without_operations(mock_migration):
    writer = MigrationWriter(mock_migration, include_header=False)
    result = writer.as_string()
    
    assert "replaces = None" not in result
    assert "initial = True" not in result
    assert "migrations.swappable_dependency" not in result
    assert "from django.conf import settings" not in result
    assert "from django.db import models" not in result
    assert "from django.db import migrations" in result
    assert "operation" not in result

def test_as_string_with_operations(mock_migration):
    mock_migration.operations = [
        migrations.RunPython(lambda: None)
    ]
    
    writer = MigrationWriter(mock_migration, include_header=False)
    result = writer.as_string()
    
    assert "def <lambda>()" in result  # Check serialized operation
    assert "migrations.RunPython" in result  # Check if RunPython imported
    assert "from django.db import migrations" in result

def test_as_string_with_dependencies(mock_migration):
    mock_migration.dependencies = [
        ("app_name", "MigrationName"),
        ("__setting__", "SOME_SETTING"),
    ]
    
    writer = MigrationWriter(mock_migration, include_header=False)
    result = writer.as_string()
    
    assert "        migrations.swappable_dependency(settings.SOME_SETTING)," in result
    assert "from django.conf import settings" in result
    assert "app_name.MigrationName" in result

def test_as_string_with_replaces(mock_migration):
    mock_migration.replaces = ("app_name", "MigrationName")
    
    writer = MigrationWriter(mock_migration, include_header=False)
    result = writer.as_string()
    
    assert "replaces = ('app_name', 'MigrationName')" in result

def test_as_string_with_initial(mock_migration):
    mock_migration.initial = True
    
    writer = MigrationWriter(mock_migration, include_header=False)
    result = writer.as_string()
    
    assert "initial = True" in result