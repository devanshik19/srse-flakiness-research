import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations import Migration

@pytest.mark.django_db
def test_migrate_forwards():
    # Arrange
    connection = connections['default']
    recorder = MigrationRecorder(connection)
    executor = MigrationExecutor(connection)
    
    # Create a User instance to ensure there's initial data
    User.objects.create_user(username='testuser', password='password')

    # Act
    state = executor.migrate(targets=[('auth', '0001_initial')])

    # Assert
    assert state is not None
    assert recorder.migration_exists('auth', '0001_initial')

@pytest.mark.django_db
def test_migrate_backwards():
    # Arrange
    connection = connections['default']
    executor = MigrationExecutor(connection)

    # Create and apply the initial migration
    executor.migrate(targets=[('auth', '0001_initial')])
    
    # Check that migration was applied
    recorder = MigrationRecorder(connection)
    assert recorder.migration_exists('auth', '0001_initial')

    # Act
    state = executor.migrate(targets=[('auth', '0001_initial')], plan=[(Migration('fake_backwards', 'auth', '0001_initial'), True)])

    # Assert
    assert state is not None
    assert not recorder.migration_exists('auth', '0001_initial')

@pytest.mark.django_db
def test_migrate_invalid_plan():
    # Arrange
    connection = connections['default']
    executor = MigrationExecutor(connection)

    # Act & Assert for InvalidMigrationPlan exception
    with pytest.raises(InvalidMigrationPlan):
        executor.migrate(targets=[('auth', '0001_initial')], plan=[(Migration('fake_forward', 'auth', '0001_initial'), False), (Migration('fake_backward', 'auth', '0001_initial'), True)])

@pytest.mark.django_db
def test_migrate_without_plan():
    # Arrange
    connection = connections['default']
    executor = MigrationExecutor(connection)

    # Initial migration
    executor.migrate(targets=[('auth', '0001_initial')])
    assert User.objects.count() == 0  # Assert no users yet

    # Act
    state = executor.migrate(targets=None)

    # Assert
    assert state is not None
    assert User.objects.count() == 0  # Still no users until migration is reapplied