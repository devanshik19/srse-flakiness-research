import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations.state import ProjectState
from django.db import router
from .exceptions import InvalidMigrationPlan

@pytest.fixture
def migration_executor():
    connection = connections['default']
    # Use MigrationLoader and MigrationRecorder to set up the context
    loader = MigrationLoader(connection)
    recorder = MigrationRecorder(connection)
    return MigrationExecutor(connection, recorder=recorder)


def test_migrate_no_plan(migration_executor):
    state = migration_executor.migrate(targets=(('auth', '0001_initial'),))
    assert isinstance(state, ProjectState)

def test_migrate_valid_plan(migration_executor):
    plan = [
        (('auth', '0001_initial'), False),
    ]
    state = migration_executor.migrate(targets=(('auth', '0001_initial'),), plan=plan)
    assert isinstance(state, ProjectState)

def test_migrate_invalid_plan(migration_executor):
    plan = [
        (('auth', '0001_initial'), False),
        (('auth', '0002_auto'), True),
    ]
    with pytest.raises(InvalidMigrationPlan):
        migration_executor.migrate(targets=(('auth', '0001_initial'),), plan=plan)

def test_migrate_with_state(migration_executor):
    state = ProjectState.from_apps(global_apps)
    state = migration_executor.migrate(targets=(('auth', '0001_initial'),), state=state)
    assert isinstance(state, ProjectState)

def test_migrate_with_fake(migration_executor):
    state = migration_executor.migrate(targets=(('auth', '0001_initial'),), fake=True)
    assert isinstance(state, ProjectState)

def test_migrate_all_backwards(migration_executor):
    # Assuming '0002_auto' is a migration that can be reverted.
    plan = [
        (('auth', '0002_auto'), True),
    ]
    state = migration_executor.migrate(targets=(('auth', '0002_auto',),), plan=plan)
    assert isinstance(state, ProjectState)

def test_migrate_with_fake_initial(migration_executor):
    state = migration_executor.migrate(targets=(('auth', '0001_initial'),), fake_initial=True)
    assert isinstance(state, ProjectState)