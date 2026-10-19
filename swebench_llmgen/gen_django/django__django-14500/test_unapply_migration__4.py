import pytest
from django.contrib.auth.models import User
from django.db import migrations
from django.db import connection
from django.apps import apps
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.state import ProjectState
from django.db.migrations.writer import MigrationWriter

@pytest.fixture
def migration_executor():
    connection = connections['default']
    recorder = MigrationRecorder(connection)
    return MigrationExecutor(connection, progress_callback=None)

def test_unapply_migration(migration_executor):
    # Setup: create initial migration that adds a user
    initial_migration = migrations.RunPython(
        lambda apps, schema_editor: User.objects.create(username='testuser'),
        reverse_code=migrations.RunPython.noop
    )
    
    # Apply the migration
    state = migration_executor._create_project_state(with_applied_migrations=[(initial_migration.app_label, initial_migration.name)])
    migration_executor.migrate([(initial_migration.app_label, initial_migration.name)], state, fake=False)
    
    # Assert the user is created
    user = User.objects.filter(username='testuser').first()
    assert user is not None
    
    # Unapply the migration
    new_state = migration_executor.unapply_migration(state, initial_migration)
    
    # Assert the user is removed after unapplied migration
    user_after_unapply = User.objects.filter(username='testuser').first()
    assert user_after_unapply is None
    
    # Check the state is updated correctly
    assert new_state.has_applied(initial_migration.app_label, initial_migration.name) is False

def test_unapply_migration_with_fake(migration_executor):
    # Setup: create initial migration that adds a user
    initial_migration = migrations.RunPython(
        lambda apps, schema_editor: User.objects.create(username='fakeuser'),
        reverse_code=migrations.RunPython.noop
    )
    
    # Apply the migration normally
    state = migration_executor._create_project_state(with_applied_migrations=[(initial_migration.app_label, initial_migration.name)])
    migration_executor.migrate([(initial_migration.app_label, initial_migration.name)], state, fake=False)
    
    # Assert the user is created
    user = User.objects.filter(username='fakeuser').first()
    assert user is not None
    
    # Unapply the migration fake
    new_state = migration_executor.unapply_migration(state, initial_migration, fake=True)
    
    # Assert the user still exists after fake unapply
    user_after_fake_unapply = User.objects.filter(username='fakeuser').first()
    assert user_after_fake_unapply is not None
    
    # Check the state is updated without actually removing the user
    assert new_state.has_applied(initial_migration.app_label, initial_migration.name) is False