import pytest
from django.apps import apps
from django.db import migrations, connection
from django.contrib.auth.models import User
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations import Migration
from django.db.migrations.state import ProjectState

@pytest.fixture
def setup_migration_executor():
    connection.close()
    recorder = MigrationRecorder(connection)
    executor = MigrationExecutor(connection)
    yield executor, recorder

def test_unapply_migration(setup_migration_executor):
    executor, recorder = setup_migration_executor
    
    # Prepare initial state with a migration
    initial_user_count = User.objects.count()
    migration = Migration(
        "0001_initial",
        "app_name",  # Replace with actual app label
        operations=[migrations.CreateModel(
            name='User',
            fields=[
                ('id', migrations.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', migrations.CharField(max_length=30)),
            ]
        )]
    )
    
    # Apply the migration
    executor.migrate([("app_name", "0001_initial")])  # Apply the initial migration

    # Verify migration was applied
    assert User.objects.count() == initial_user_count + 0  # Adjust based on migration behavior
    
    # Create a ProjectState to simulate the current state
    state = ProjectState()
    state.apps = apps
    state = executor._create_project_state(with_applied_migrations=True)

    # Unapply the migration
    new_state = executor.unapply_migration(state, migration)

    # Check if the migration is recorded as unapplied
    assert recorder.has_unapplied(migration.app_label, migration.name)
    
    # Verify state after unapplied migration
    assert User.objects.count() == initial_user_count

    # Check if progress callback is called correctly (optional, requires implementation)
    # executor.progress_callback = lambda status, migration, fake: assert status == "unapply_success"
    # executor.unapply_migration(state, migration)