import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations import Migration
from django.db import router
from django.apps.registry import apps as global_apps
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.exceptions import InvalidMigrationPlan

def test_migrate_no_plan():
    executor = MigrationExecutor(connection)
    state = executor.migrate(targets=[], plan=None, state=None)
    assert state is not None
    assert isinstance(state, ProjectState)

def test_migrate_all_forwards():
    # Assume there exists a migration for User model.
    executor = MigrationExecutor(connection)
    targets = ('auth', '0001_initial')  # Example for migrating the auth app
    state_before = executor.migrate(targets=targets, plan=None)
    assert state_before != executor._create_project_state(with_applied_migrations=True)

def test_migrate_all_backwards():
    executor = MigrationExecutor(connection)
    # Define a migration plan to go backwards if possible
    plan = [(Migration('0001_initial', 'auth'), True)]
    with pytest.raises(InvalidMigrationPlan):
        executor.migrate(targets=None, plan=plan)

def test_migrate_mixed_plan():
    executor = MigrationExecutor(connection)
    plan = [
        (Migration('0001_initial', 'auth'), False),  # Forward migration
        (Migration('0002_auto', 'auth'), True)      # Backward migration
    ]
    with pytest.raises(InvalidMigrationPlan):
        executor.migrate(targets=None, plan=plan)

def test_migrate_fake_initial():
    executor = MigrationExecutor(connection)
    targets = ('auth', '0001_initial')
    state = executor.migrate(targets=targets, plan=None, fake=True)
    assert state is not None  # It should run without error even with fake

def test_migrate_with_applied_migrations():
    executor = MigrationExecutor(connection)
    User.objects.create(username='testuser')  # Apply a migration by creating a user
    targets = ('auth', '0001_initial')
    state = executor.migrate(targets=targets, plan=None)
    assert state is not None
    assert 'auth.0001_initial' in state.applied