import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import QuerySet

# Assuming QuerySet has been imported from the correct path

def test_bulk_create_with_valid_data():
    # Arrange
    users = [User(username=f'user{i}', email=f'user{i}@example.com') for i in range(5)]
    queryset = User.objects

    # Act
    created_users = queryset.bulk_create(users)

    # Assert
    assert len(created_users) == len(users)
    for user in created_users:
        assert user.pk is not None
        assert user.username.startswith('user')

def test_bulk_create_empty_list():
    # Arrange
    queryset = User.objects

    # Act
    created_users = queryset.bulk_create([])

    # Assert
    assert created_users == []

def test_bulk_create_with_invalid_batch_size():
    # Arrange
    users = [User(username='invalid_user', email='invalid_user@example.com')]
    queryset = User.objects

    # Act & Assert
    with pytest.raises(ValueError, match="Batch size must be a positive integer."):
        queryset.bulk_create(users, batch_size=0)

def test_bulk_create_with_invalid_model_inheritance():
    # Arrange
    # Create a subclass to simulate multi-table inheritance
    class MultiTableUser(User):
        pass

    queryset = QuerySet(MultiTableUser)

    # Act & Assert
    with pytest.raises(ValueError, match="Can't bulk create a multi-table inherited model"):
        queryset.bulk_create([MultiTableUser(username='user1', email='user1@example.com')])

def test_bulk_create_with_conflict_handling():
    # Arrange
    existing_user = User.objects.create(username='user1', email='user1@example.com')
    users = [
        User(username='user1', email='user1@newdomain.com'),  # Conflict
        User(username='user2', email='user2@example.com')
    ]
    queryset = User.objects
    
    # Act
    created_users = queryset.bulk_create(users, ignore_conflicts=True)

    # Assert
    assert len(created_users) == 2
    assert created_users[0].email == 'user1@newdomain.com'  # Conflict is ignored
    assert created_users[1].pk is not None