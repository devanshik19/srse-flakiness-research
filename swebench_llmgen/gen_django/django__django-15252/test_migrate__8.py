import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations.state import ProjectState
from django.apps.registry import apps as global_apps
from django.db import router

@pytest.fixture
def migration_executor():
    connection = connections['default']
    recorder = MigrationRecorder(connection)
    loader = MigrationLoader(connection, ignore_no_migrations=True)
    return MigrationExecutor(connection, recorder, loader)

def test_migrate_no_targets(migration_executor):
    initial_state = migration_executor._create_project_state(with_applied_migrations=True)
    state = migration_executor.migrate(targets=[], state=initial_state)

    assert isinstance(state, ProjectState)
    assert state.has_migrations()  # Check that it reflects the applied migrations

def test_migrate_with_forwards(migration_executor):
    migration_executor.migrate(targets=['auth.0001_initial'])  # Ensure this migration is applied
    state = migration_executor.migrate(targets=['auth.0002_auto_000101_1234'])

    assert isinstance(state, ProjectState)
    assert 'auth.0002_auto_000101_1234' in state.applied

def test_migrate_with_backwards(migration_executor):
    migration_executor.migrate(targets=['auth.0002_auto_000101_1234'])  # Apply a forward migration
    state = migration_executor.migrate(targets=['auth.0001_initial'], plan=[('auth.0002_auto_000101_1234', True)])

    assert isinstance(state, ProjectState)
    assert 'auth.0001_initial' in state.applied
    assert 'auth.0002_auto_000101_1234' not in state.applied

def test_migrate_mixed_plan_raises(migration_executor):
    migration_executor.migrate(targets=['auth.0001_initial'])  # Apply initial migration
    with pytest.raises(InvalidMigrationPlan):
        migration_executor.migrate(targets=['auth.0001_initial', 'auth.0002_auto_000101_1234'], 
                                   plan=[('auth.0001_initial', False), ('auth.0002_auto_000101_1234', True)])

def test_migrate_empty_plan_creates_state(migration_executor):
    state = migration_executor.migrate(targets=[], plan=[])

    assert isinstance(state, ProjectState)
    assert state.has_migrations()  # Should reflect an empty state without errors

def test_migrate_with_fake(migration_executor):
    migration_executor.migrate(targets=['auth.0001_initial'], fake=True)  # Apply initial migration as fake
    state = migration_executor.migrate(targets=[], state=None)

    assert isinstance(state, ProjectState)
    assert 'auth.0001_initial' in state.applied  # Should reflect the fake applied migration