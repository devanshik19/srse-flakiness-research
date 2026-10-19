import pytest
from django.contrib.auth.models import User
from django.db import migrations
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations.state import ProjectState

@pytest.fixture
def migration_executor(connection):
    recorder = MigrationRecorder(connection)
    return MigrationExecutor(connection, progress_callback=lambda *_: None)

@pytest.fixture
def user_instance():
    return User.objects.create(username='testuser', password='password')

def unapply_migration_with_success(state, migration_executor, migration, fake=False):
    state = migration_executor.unapply_migration(state, migration, fake)
    return state

def test_unapply_migration(migration_executor, user_instance):
    # Create a mock migration
    migration = migrations.Migration('0001_initial', 'auth')
    
    # Prepare initial state and apply the migration
    initial_state = ProjectState()
    ProjectState.set_all_apps_with_migrations({user_instance._meta.app_label: {migration.name: migration}})
    
    migration_executor.migrate([migration])
    
    assert user_instance.objects.count() == 1  # Ensure the user was created

    # Unapply the migration
    state = unapply_migration_with_success(initial_state, migration_executor, migration)

    assert user_instance.objects.count() == 0  # Ensure the user was deleted
    assert migration_executor.recorder.has_recorded_unapplied(migration.app_label, migration.name)

def test_unapply_migration_with_replacement(migration_executor, user_instance):
    # Create a mock migration with a replacement
    migration = migrations.Migration('0001_initial', 'auth', replaces=[('auth', '0001_initial')])
    
    # Prepare initial state and apply the migration
    initial_state = ProjectState()
    ProjectState.set_all_apps_with_migrations({user_instance._meta.app_label: {migration.name: migration}})
    
    migration_executor.migrate([migration])
    
    assert user_instance.objects.count() == 1  # Ensure the user was created

    # Unapply the migration
    state = unapply_migration_with_success(initial_state, migration_executor, migration)

    assert user_instance.objects.count() == 0  # Ensure the user was deleted
    assert migration_executor.recorder.has_recorded_unapplied('auth', '0001_initial')