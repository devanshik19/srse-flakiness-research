import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.exceptions import InvalidMigrationPlan
from django.db.migrations.loader import MigrationLoader


@pytest.fixture
def migration_executor():
    connection = connections['default']
    return MigrationExecutor(connection)


def test_migrate_no_plan(migration_executor):
    # Initial state with no migrations applied
    targets = [ ('app_name', '0001_initial') ]  # Adjust according to your app migrations
    state = migration_executor.migrate(targets)
    assert state  # Check if state is not None


def test_migrate_all_forwards(migration_executor):
    targets = [ ('app_name', '0002_auto') ]  # Adjust according to your app migrations
    plan = migration_executor.migration_plan(targets)
    
    state = migration_executor.migrate(targets, plan=plan)
    assert state  # Check if state is returned


def test_migrate_all_backwards(migration_executor):
    targets = [ ('app_name', '0001_initial') ]  # Adjust according to your app migrations
    plan = migration_executor.migration_plan(targets)  
    
    # First apply migration, then unapply it
    migration_executor.migrate(targets, plan=plan)
    state = migration_executor.migrate(targets, plan=[(migration, True) for migration in plan])
    assert state  # Check if state is returned


def test_migrate_mixed_plan_raises_exception(migration_executor):
    targets_forward = [('app_name', '0001_initial')]
    targets_backward = [('app_name', '0002_auto')]
    
    plan_forward = migration_executor.migration_plan(targets_forward)
    plan_backward = migration_executor.migration_plan(targets_backward)

    with pytest.raises(InvalidMigrationPlan):
        migration_executor.migrate(targets_forward, plan=plan_forward + plan_backward)


def test_migrate_with_fake(migration_executor):
    targets = [('app_name', '0002_auto')]  # Adjust according to your app migrations
    plan = migration_executor.migration_plan(targets)

    state = migration_executor.migrate(targets, plan=plan, fake=True)
    assert state  # Check if state is returned