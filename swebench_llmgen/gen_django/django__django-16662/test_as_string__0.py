import pytest
from django.db import migrations
from django.contrib.auth.models import User
from django.utils.timezone import now
from django import get_version
from django.db.migrations.writer import MigrationWriter

@pytest.fixture
def migration_fixture():
    migration = migrations.Migration("0001_initial", "app_name")
    migration.operations = []
    migration.dependencies = []
    migration.replaces = None
    migration.initial = False
    return migration

def test_as_string(migration_fixture):
    writer = MigrationWriter(migration=migration_fixture, include_header=True)
    
    result = writer.as_string()
    
    assert "initial" not in result
    assert "replaces" not in result
    assert "from django.db import migrations" in result
    assert "VERSION" in result  # Checks if Django version info is included
    assert "timestamp" in result  # Checks if timestamp is included
    
    # Test case for migrations with operations
    migration_fixture.operations.append(migrations.RunPython('some_func'))
    migration_fixture.dependencies.append(('app_name', '0001_initial'))
    writer_with_ops = MigrationWriter(migration=migration_fixture, include_header=True)
    
    result_with_ops = writer_with_ops.as_string()

    assert "some_func" in result_with_ops
    assert "app_name" in result_with_ops
    assert "\n    initial = True\n" not in result_with_ops  # Check initial not set
    
    # Testing with replaces
    migration_fixture.replaces = ('app_name', '0001_prev')
    writer_with_replaces = MigrationWriter(migration=migration_fixture, include_header=True)
    
    result_with_replaces = writer_with_replaces.as_string()
    
    assert "replaces = ('app_name', '0001_prev')" in result_with_replaces