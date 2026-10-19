import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.exceptions import InvalidMigrationPlan
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder

@pytest.fixture
def migration_executor():
    connection = connections['default']
    recorder = MigrationRecorder(connection)
    loader = MigrationLoader(connection)

    executor = MigrationExecutor(connection)
    executor.recorder = recorder
    executor.loader = loader
    return executor

def test_migrate_no_targets(migration_executor):
    state = migration_executor.migrate(targets=[], plan=None, state=None)
    assert state is not None  # Assert state is returned

def test_migrate_forward(migration_executor):
    User.objects.create(username='testuser')
    plan = [(('auth', '0001_initial'), False)]  # Assume this migration exists

    state = migration_executor.migrate(targets=[('auth', '0001_initial')], plan=plan)
    assert state is not None  # Assert state is returned
    assert User.objects.filter(username='testuser').exists()  # Migration should have applied

def test_migrate_backward(migration_executor):
    User.objects.create(username='testuser')
    plan = [(('auth', '0001_initial'), True)]  # Migration should reverse

    state = migration_executor.migrate(targets=[('auth', '0001_initial')], plan=plan)
    assert state is not None  # Assert state is returned
    assert not User.objects.filter(username='testuser').exists()  # Migration should have un-applied

def test_migrate_invalid_plan(migration_executor):
    plan = [(('auth', '0001_initial'), False), (('auth', '0001_initial'), True)]

    with pytest.raises(InvalidMigrationPlan):
        migration_executor.migrate(targets=[('auth', '0001_initial')], plan=plan)

def test_migrate_with_state(migration_executor):
    User.objects.create(username='testuser')
    state_before = migration_executor._create_project_state(with_applied_migrations=True)
    
    plan = [(('auth', '0001_initial'), False)]
    state_after = migration_executor.migrate(targets=[('auth', '0001_initial')], plan=plan, state=state_before)
  
    assert state_after != state_before  # Ensure the state changed
    assert User.objects.filter(username='testuser').exists()  # Migration should have applied