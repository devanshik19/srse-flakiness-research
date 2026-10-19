import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F

@pytest.fixture
def user_instance():
    user = User(username='testuser', email='test@example.com')
    user.save()
    return user

def test_bulk_update_valid(user_instance):
    # Create multiple user instances
    users = [
        User(username='user1', email='user1@example.com'),
        User(username='user2', email='user2@example.com'),
        User(username='user3', email='user3@example.com'),
    ]
    User.objects.bulk_create(users)

    # Prepare bulk update
    for user in users:
        user.email = f'updated_{user.username}@example.com'
    
    # Perform bulk update
    updated_count = User.objects.bulk_update(users, ['email'])

    assert updated_count == len(users)
    for user in users:
        user.refresh_from_db()
        assert user.email == f'updated_{user.username}@example.com'

def test_bulk_update_empty_fields(user_instance):
    users = [
        User(username='user1', email='user1@example.com'),
        User(username='user2', email='user2@example.com')
    ]
    User.objects.bulk_create(users)

    with pytest.raises(ValueError, match='Field names must be given to bulk_update().'):
        User.objects.bulk_update(users, [])

def test_bulk_update_no_primary_key(user_instance):
    users = [
        User(username='user1', email='user1@example.com'),
        User(username='user2', email='user2@example.com')
    ]

    with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
        User.objects.bulk_update(users, ['email'])

def test_bulk_update_invalid_field(user_instance):
    users = [
        User(username='user1', email='user1@example.com'),
        User(username='user2', email='user2@example.com')
    ]
    User.objects.bulk_create(users)

    with pytest.raises(ValueError, match='bulk_update() can only be used with concrete fields.'):
        User.objects.bulk_update(users, ['username'])

def test_bulk_update_with_primary_key_field(user_instance):
    users = [
        User(username='user1', email='user1@example.com'),
        User(username='user2', email='user2@example.com')
    ]
    User.objects.bulk_create(users)

    with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
        User.objects.bulk_update(users, ['id'])