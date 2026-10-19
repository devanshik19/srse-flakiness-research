import pytest
from django.contrib.auth.models import User
from django.db import migrations
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations.loader import MigrationLoader
from django.db import connection


@pytest.fixture
def migration_executor():
    recorder = MigrationRecorder(connection)
    return MigrationExecutor(connection=connection, progress_callback=None)


@pytest.fixture
def user_migration():
    # Create a migration for creating the User model
    return migrations.CreateModel(
        name='User',
        fields=[
            ('id', migrations.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
            ('username', migrations.CharField(max_length=150, unique=True)),
        ],
        options={
            'db_table': 'auth_user',
        },
    )


def test_unapply_migration(migration_executor, user_migration):
    # Apply the migration first
    migration_executor.apply_migration(ProjectState(), user_migration)
    
    # Check if migration applied
    assert User.objects.exists()

    # Now unapply the migration
    state = ProjectState()
    new_state = migration_executor.unapply_migration(state, user_migration)

    # Check if migration has been unapplied
    assert not User.objects.exists()
    
    # Check that the new state reflects the unapplication
    assert not new_state.has_model('auth.User')


def test_unapply_migration_fake(migration_executor, user_migration):
    # Apply the migration first
    migration_executor.apply_migration(ProjectState(), user_migration)
    
    # Check if migration applied
    assert User.objects.exists()

    # Now unapply the migration with fake=True
    state = ProjectState()
    new_state = migration_executor.unapply_migration(state, user_migration, fake=True)

    # Check if the objects still exist as we did it fake
    assert User.objects.exists()

    # Check that the new state reflects the unapplication
    assert new_state.has_model('auth.User')