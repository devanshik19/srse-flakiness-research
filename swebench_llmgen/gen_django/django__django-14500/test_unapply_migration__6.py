import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations import Migration
from django.db import models

@pytest.fixture
def migration_executor():
    connection = connections['default']
    return MigrationExecutor(connection)

@pytest.fixture
def sample_migration():
    class SampleMigration(Migration):
        dependencies = []
        operations = []
        
        def unapply(self, state, schema_editor):
            # Dummy unapply logic, acts as if it removed a field
            return state

    return SampleMigration(app_label='auth', name='0001_initial')

@pytest.fixture
def project_state():
    # Create project state for testing
    return MigrationLoader(connections['default']).project_state()

def test_unapply_migration_success(migration_executor, sample_migration, project_state):
    migration_executor.recorder = MagicMock()
    migration_executor.progress_callback = MagicMock()
    
    state = project_state
    
    # Test unapplying a migration
    new_state = migration_executor.unapply_migration(state, sample_migration, fake=False)
    
    assert new_state == state  # Ensure the state unmodified for the dummy migration logic
    migration_executor.recorder.record_unapplied.assert_called_once_with('auth', '0001_initial')
    migration_executor.progress_callback.assert_called_with("unapply_success", sample_migration, False)

def test_unapply_migration_fake(migration_executor, sample_migration, project_state):
    migration_executor.recorder = MagicMock()
    migration_executor.progress_callback = MagicMock()
    
    state = project_state
    
    # Test unapplying a migration with fake set to True
    new_state = migration_executor.unapply_migration(state, sample_migration, fake=True)
    
    assert new_state == state  # Ensure the state is still unchanged
    migration_executor.recorder.record_unapplied.assert_called_once_with('auth', '0001_initial')
    migration_executor.progress_callback.assert_called_with("unapply_success", sample_migration, True)