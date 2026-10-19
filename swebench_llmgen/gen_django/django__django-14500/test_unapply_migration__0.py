import pytest
from django.apps import apps
from django.contrib.auth.models import User
from django.db import migrations
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations.state import ProjectState

class FakeMigration:
    def __init__(self, app_label, name, replaces=None, atomic=True):
        self.app_label = app_label
        self.name = name
        self.replaces = replaces
        self.atomic = atomic

    def unapply(self, state, schema_editor):
        # Simulate unapplying by returning the state unchanged for this test
        return state

@pytest.fixture
def migration_executor():
    connection = migrations.get_connection()
    recorder = MigrationRecorder(connection)
    return MigrationExecutor(connection=connection, progress_callback=None, recorder=recorder)

def test_unapply_migration(migration_executor):
    user_migration = FakeMigration(app_label='auth', name='0001_initial')
    initial_state = ProjectState()
    
    # Test unapplying a migration normally
    new_state = migration_executor.unapply_migration(initial_state, user_migration, fake=False)
    assert new_state == initial_state
    
    # Test unapplying with a replacement migration
    replacement_migration = FakeMigration(app_label='auth', name='0001_initial', replaces=[('auth', '0001_initial')])
    new_state = migration_executor.unapply_migration(initial_state, replacement_migration, fake=False)
    assert new_state == initial_state

    # Verify the recorder recorded the unapplied migrations correctly
    assert migration_executor.recorder.has_recorded_unapplied('auth', '0001_initial')
    assert migration_executor.recorder.has_recorded_unapplied('auth', '0001_initial')

    # Test unapplying migration with fake option
    new_state_fake = migration_executor.unapply_migration(initial_state, user_migration, fake=True)
    assert new_state_fake == initial_state