import pytest
from django.db import migrations
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.module_loading import import_module

from django.db.migrations.writer import MigrationWriter

@pytest.fixture
def migration_without_operations():
    return migrations.Migration(
        name='MigrationTest', 
        app_label='auth', 
        operations=[], 
        dependencies=[]
    )

@pytest.fixture
def migration_with_operations():
    return migrations.Migration(
        name='MigrationTestWithOps', 
        app_label='auth', 
        operations=[
            migrations.CreateModel(
                name='TestModel', 
                fields=[
                    ('field1', models.CharField(max_length=100)),
                ]
            ),
        ], 
        dependencies=[]
    )

def test_as_string_empty_migration(migration_without_operations):
    writer = MigrationWriter(migration=migration_without_operations, include_header=False)
    result = writer.as_string()
    
    assert "operations" not in result
    assert "imports" in result
    assert "dependencies" in result
    assert "initial" not in result
    assert "replaces" not in result

def test_as_string_with_operations(migration_with_operations):
    writer = MigrationWriter(migration=migration_with_operations, include_header=False)
    result = writer.as_string()
    
    assert "operations" in result
    assert "CreateModel" in result
    assert "TestModel" in result
    assert "dependencies" not in result
    assert "initial" not in result
    assert "replaces" not in result

def test_as_string_with_dependencies(migration_with_operations):
    migration_with_dependencies = migrations.Migration(
        name='MigrationTestWithDeps', 
        app_label='auth', 
        operations=[], 
        dependencies=[('auth', '0001_initial')]
    )
    
    writer = MigrationWriter(migration=migration_with_dependencies, include_header=False)
    result = writer.as_string()
    
    assert "dependencies" in result
    assert "auth" in result

def test_as_string_initial_flag(migration_without_operations):
    migration_with_initial = migrations.Migration(
        name='InitialMigration', 
        app_label='auth', 
        operations=[], 
        dependencies=[],
        initial=True
    )
    
    writer = MigrationWriter(migration=migration_with_initial, include_header=False)
    result = writer.as_string()
    
    assert "initial = True" in result

def test_as_string_with_replaces(migration_without_operations):
    migration_with_replaces = migrations.Migration(
        name='MigrationWithReplaces', 
        app_label='auth', 
        operations=[], 
        dependencies=[],
        replaces=[('auth', '0001_initial')]
    )
    
    writer = MigrationWriter(migration=migration_with_replaces, include_header=False)
    result = writer.as_string()
    
    assert "replaces = ('auth', '0001_initial')" in result