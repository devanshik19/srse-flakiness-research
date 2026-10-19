import pytest
from django.apps import apps
from django.contrib.auth.models import User
from django.db import migrations
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.recorder import MigrationRecorder
from django.db import connection

@pytest.fixture
def migration_executor():
    """Fixture to provide an instance of MigrationExecutor."""
    recorder = MigrationRecorder(connection)
    return MigrationExecutor(connection, progress_callback=None)

def test_unapply_migration_with_fake(migration_executor):
    """Test unapply_migration with fake flag set to True."""
    user = User.objects.create(username='testuser')
    migration = migrations.Migration('0001_initial', 'auth')  # assuming this migration exists
    state = apps.get_app_config('auth').migration_cache['0001_initial']
    
    new_state = migration_executor.unapply_migration(state, migration, fake=True)

    # Ensure the state is returned as is since it's a fake unapply
    assert new_state == state
    assert MigrationRecorder.objects.filter(app='auth', name='0001_initial').exists()

def test_unapply_migration_without_fake(migration_executor):
    """Test unapply_migration without using fake."""
    user = User.objects.create(username='testuser')
    user.save()  # Ensure migration has applied

    migration = migrations.Migration('0001_initial', 'auth')  # assuming this migration exists
    state = apps.get_app_config('auth').migration_cache['0001_initial']
    
    new_state = migration_executor.unapply_migration(state, migration, fake=False)

    # Ensure the state has changed after unapplying the migration
    assert not User.objects.filter(username='testuser').exists()
    assert MigrationRecorder.objects.filter(app='auth', name='0001_initial').exists()

def test_unapply_migration_records_replaces(migration_executor):
    """Test unapply_migration logic with replacement migrations."""
    # Mock migration with replacements
    class ReplacementMigration:
        app_label = 'auth'
        name = '0001_initial'
        replaces = [('auth', '0001_initial')]

        @staticmethod
        def unapply(state, schema_editor):
            return state  # No-op for this test
    
    migration = ReplacementMigration()
    state = apps.get_app_config('auth').migration_cache['0001_initial']
    
    new_state = migration_executor.unapply_migration(state, migration)

    # Check if it recorded both replacements
    assert MigrationRecorder.objects.filter(app='auth', name='0001_initial').exists()
    
    # Test if progress callback would normally be called (not actually testing execution of callback here)
    assert migration_executor.recorder.record_unapplied.return_value is None