import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations.state import ProjectState
from django.db import migrations


@pytest.mark.parametrize("targets, plan, state, fake, fake_initial, expected_state", [
    (['auth.0001_initial'], None, None, False, False, 'expected_state_after_migration_1'),
    (['auth.0002_auto_20200101_1234'], None, None, False, False, 'expected_state_after_migration_2'),
    ([], [], None, False, False, 'expected_state_empty_plan'),
])
def test_migrate(targets, plan, state, fake, fake_initial, expected_state):
    connection = connections['default']
    executor = MigrationExecutor(connection)
    
    # Ensure the schema is present
    executor.recorder.ensure_schema()
    
    # Prepare the initial state
    if state is None:
        state = executor._create_project_state(with_applied_migrations=True)
    
    # Check that the migrate method does not raise exceptions and returns a valid state
    new_state = executor.migrate(targets, plan=plan, state=state, fake=fake, fake_initial=fake_initial)
    
    # Validate that the new_state matches the expected state
    assert new_state == expected_state


def test_migrate_invalid_plan():
    connection = connections['default']
    executor = MigrationExecutor(connection)
    
    # Prepare a mixed plan (both forwards and backwards)
    plan = [(migrations.Migration('auth', '0001_initial'), False),
            (migrations.Migration('auth', '0002_auto_20200101_1234'), True)]
    
    with pytest.raises(InvalidMigrationPlan):
        executor.migrate([], plan=plan)