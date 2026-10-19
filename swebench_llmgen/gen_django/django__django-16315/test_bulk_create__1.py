import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError

@pytest.fixture
def user_data():
    return [
        User(username='user1', email='user1@example.com'),
        User(username='user2', email='user2@example.com'),
        User(username='user3', email='user3@example.com'),
    ]

def test_bulk_create_valid(user_data):
    queryset = User.objects
    users = queryset.bulk_create(user_data)
    
    assert len(users) == 3
    assert User.objects.count() == 3

def test_bulk_create_with_batch_size(user_data):
    queryset = User.objects
    users = queryset.bulk_create(user_data, batch_size=2)

    assert len(users) == 3
    assert User.objects.count() == 3

def test_bulk_create_ignore_conflicts(user_data):
    queryset = User.objects
    User.objects.bulk_create(user_data)

    # Attempt to bulk create again with a conflict
    users_with_conflict = [
        User(username='user1', email='user1_conflict@example.com'),
        User(username='user2', email='user2_conflict@example.com'),
    ]
    users = queryset.bulk_create(users_with_conflict, ignore_conflicts=True)

    assert len(users) == 2
    assert User.objects.count() == 3  # original 3 should be unchanged

def test_bulk_create_raises_value_error_on_invalid_batch_size(user_data):
    queryset = User.objects
    
    with pytest.raises(ValueError, match="Batch size must be a positive integer."):
        queryset.bulk_create(user_data, batch_size=0)

    with pytest.raises(ValueError, match="Batch size must be a positive integer."):
        queryset.bulk_create(user_data, batch_size=-1)

def test_bulk_create_multi_table_inheritance(user_data):
    # Test case to simulate creating users from an inherited model
    User.objects.bulk_create(user_data)
    
    class InheritedUser(User):
        pass  # Simulates a multi-table inheritance
     
    with pytest.raises(ValueError, match="Can't bulk create a multi-table inherited model"):
        queryset = InheritedUser.objects
        queryset.bulk_create(user_data)