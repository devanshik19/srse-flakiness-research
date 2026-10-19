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

def test_bulk_create_success(user_data):
    queryset = User.objects
    created_users = queryset.bulk_create(user_data)
    
    assert len(created_users) == len(user_data)
    assert User.objects.count() == len(user_data)

    for user in created_users:
        assert User.objects.filter(username=user.username).exists()

def test_bulk_create_with_empty_list(user_data):
    queryset = User.objects
    created_users = queryset.bulk_create([])

    assert created_users == []
    assert User.objects.count() == len(user_data)

def test_bulk_create_with_invalid_batch_size(user_data):
    queryset = User.objects
    with pytest.raises(ValueError, match="Batch size must be a positive integer."):
        queryset.bulk_create(user_data, batch_size=0)

def test_bulk_create_with_ignore_conflicts(user_data):
    queryset = User.objects
    queryset.bulk_create(user_data)

    user_with_conflict = User(username='user1', email='user1@conflict.com')
    created_users = queryset.bulk_create([user_with_conflict], ignore_conflicts=True)

    assert len(created_users) == 1
    assert User.objects.filter(username='user1', email='user1@conflict.com').exists()

def test_bulk_create_with_update_conflicts(user_data):
    queryset = User.objects
    queryset.bulk_create(user_data)

    user_with_conflict = User(username='user1', email='user1@conflict.com')
    created_users = queryset.bulk_create([user_with_conflict], update_conflicts=True, unique_fields=['username'])

    assert len(created_users) == 1
    assert User.objects.get(username='user1').email == 'user1@conflict.com'