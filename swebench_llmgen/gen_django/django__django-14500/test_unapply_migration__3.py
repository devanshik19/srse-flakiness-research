import pytest
from django.apps.registry import apps
from django.contrib.auth.models import User
from django.db import migrations, connection
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.state import ProjectState
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations.loader import MigrationLoader


@pytest.fixture
def migration_executor():
    recorder = MigrationRecorder(connection)
    return MigrationExecutor(connection=connection, progress_callback=None)


@pytest.fixture
def user_migration():
    return User.objects.create(username="testuser", password="password")


@pytest.fixture
def project_state():
    return ProjectState()


def test_unapply_migration(migration_executor, user_migration, project_state):
    migration_loader = MigrationLoader(connection)
    initial_state = migration_loader.project_state(apps)
    
    migration = migration_loader.get_migration("auth", "0001_initial")
    migration_executor.migrate([migration], initial_state, fake=False)
    
    assert User.objects.count() == 1  # Check the user is created

    # Now, unapply the migration
    new_state = migration_executor.unapply_migration(state=initial_state, migration=migration, fake=False)

    assert User.objects.count() == 0  # Check the user is deleted
    assert new_state != initial_state  # Ensure the state has changed

    # Ensure that the migration is recorded as unapplied
    assert migration_executor.recorder.has_unapplied(migration)