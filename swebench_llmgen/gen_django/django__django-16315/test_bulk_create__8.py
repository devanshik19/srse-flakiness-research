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
    users = User.objects.bulk_create(user_data)
    assert User.objects.count() == 3
    assert users[0].pk is not None
    assert users[1].pk is not None
    assert users[2].pk is not None

def test_bulk_create_empty_list():
    result = User.objects.bulk_create([])
    assert result == []

def test_bulk_create_batch_size(user_data):
    users = User.objects.bulk_create(user_data, batch_size=2)
    assert User.objects.count() == 3

def test_bulk_create_ignore_conflicts(user_data):
    User.objects.bulk_create(user_data)
    with pytest.raises(IntegrityError):
        User.objects.bulk_create([User(username='user1', email='user1@example.com')], ignore_conflicts=False)
    users_with_conflict = User.objects.bulk_create([User(username='user1', email='user1_replaced@example.com')], ignore_conflicts=True)
    assert User.objects.filter(username='user1_replaced@example.com').exists()

def test_bulk_create_with_unique_fields(user_data):
    user1 = User(username='user1', email='user1@example.com')
    User.objects.bulk_create([user1])
    user2 = User(username='user1', email='user2@example.com')
  
    assert User.objects.bulk_create([user2], unique_fields=['username'])[0].pk is None  # Conflict should prevent user2 from being created
    assert User.objects.count() == 1  # Only user1 should exist