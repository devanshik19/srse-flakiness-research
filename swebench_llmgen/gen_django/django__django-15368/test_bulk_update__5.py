import pytest
from django.contrib.auth.models import User
from django.db import transaction

@pytest.fixture
def users():
    user1 = User.objects.create(username='user1', email='user1@example.com')
    user2 = User.objects.create(username='user2', email='user2@example.com')
    return [user1, user2]

def test_bulk_update(users):
    # Test updating valid fields
    users[0].email = 'user1_updated@example.com'
    users[1].email = 'user2_updated@example.com'
    
    updated_count = User.objects.bulk_update(users, ['email'])
    
    assert updated_count == 2
    assert User.objects.get(pk=users[0].pk).email == 'user1_updated@example.com'
    assert User.objects.get(pk=users[1].pk).email == 'user2_updated@example.com'

def test_bulk_update_with_empty_fields(users):
    with pytest.raises(ValueError, match='Field names must be given to bulk_update().'):
        User.objects.bulk_update(users, [])

def test_bulk_update_with_none_primary_key():
    user = User(username='user3', email='user3@example.com')  # Not saved yet
    with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
        User.objects.bulk_update([user], ['email'])

def test_bulk_update_with_negative_batch_size(users):
    with pytest.raises(ValueError, match='Batch size must be a positive integer.'):
        User.objects.bulk_update(users, ['email'], batch_size=-1)

def test_bulk_update_with_non_concrete_field(users):
    user = User(username='user4', email='user4@example.com')
    user.save()
    
    with pytest.raises(ValueError, match='bulk_update() can only be used with concrete fields.'):
        User.objects.bulk_update([user], ['date_joined'])  # date_joined is a non-concrete field

def test_bulk_update_with_primary_key_field(users):
    with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
        User.objects.bulk_update(users, ['id'])  # id is the primary key field