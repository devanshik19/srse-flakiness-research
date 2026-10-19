import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations.state import ProjectState
from django.db.migrations.exceptions import InvalidMigrationPlan

@pytest.fixture
def migration_executor():
    recorder = MigrationRecorder(connection)
    loader = MigrationLoader(connection)
    executor = MigrationExecutor(connection)
    executor.recorder = recorder
    executor.loader = loader
    return executor

def test_migrate_no_plan(migration_executor):
    User.objects.create_user(username='testuser', password='testpass')
    targets = [('auth', '0001_initial')]
    state = migration_executor.migrate(targets)

    assert state is not None
    assert User.objects.all().exists()

def test_migrate_with_plan(migration_executor):
    targets = [('auth', '0001_initial')]
    migration_plan = migration_executor.migration_plan(targets)
    state = migration_executor.migrate(targets, plan=migration_plan)

    assert state is not None
    assert state.has_table('auth_user')

def test_migrate_with_invalid_plan(migration_executor):
    targets = [('auth', '0001_initial')]
    migration_plan = migration_executor.migration_plan(targets)
    
    # Create a mixed plan with both forward and backward migrations
    mixed_plan = [(migration_plan[0][0], False), (migration_plan[0][0], True)]
    
    with pytest.raises(InvalidMigrationPlan):
        migration_executor.migrate(targets, plan=mixed_plan)

def test_migrate_fake(migration_executor):
    # Ensure user model exists before 'faking' a migration
    User.objects.create_user(username='testuser', password='testpass')
    targets = [('auth', '0001_initial')]
    
    # Fake migration
    state = migration_executor.migrate(targets, fake=True)

    assert state is not None
    assert User.objects.all().exists()

def test_migrate_with_state(migration_executor):
    User.objects.create_user(username='testuser', password='testpass')
    targets = [('auth', '0001_initial')]
    initial_state = migration_executor._create_project_state(with_applied_migrations=False)

    state = migration_executor.migrate(targets, state=initial_state)

    assert state is not None
    assert state.has_table('auth_user')