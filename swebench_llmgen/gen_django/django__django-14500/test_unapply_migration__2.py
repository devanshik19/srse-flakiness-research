import pytest
from django.apps import apps
from django.contrib.auth.models import User
from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations import Migration
from django.db.migrations.recorder import MigrationRecorder
from django.db import transaction

# Create a sample migration for testing
class TestMigration(Migration):
    dependencies = []
    operations = []

    def unapply(self, state, schema_editor):
        # Example of unapplying a migration, here we just simulate a change
        User.objects.filter(username='testuser').delete()
        return state

@pytest.fixture
def migration_executor():
    connection = connections['default']
    recorder = MigrationRecorder(connection)
    executor = MigrationExecutor(connection, progress_callback=None)
    return executor, recorder

@pytest.fixture
def test_user():
    user = User.objects.create(username='testuser')
    return user

@pytest.mark.parametrize("fake", [True, False])
def test_unapply_migration(migration_executor, test_user, fake):
    executor, recorder = migration_executor
    migration = TestMigration('0001_test', 'testapp')
    # Pretend the migration has been applied
    recorder.record_applied('testapp', '0001_test')

    # Pre-check: User should exist before unapplying migration
    assert User.objects.filter(username='testuser').exists()

    # Unapply the migration
    state = executor.unapply_migration(None, migration, fake=fake)

    # Post-check: User should not exist after unapplying migration
    assert not User.objects.filter(username='testuser').exists()

    # Check if the recorder recorded the unapplied migration
    recorded_migrations = recorder.unapplied_migrations()
    assert (migration.app_label, migration.name) in recorded_migrations