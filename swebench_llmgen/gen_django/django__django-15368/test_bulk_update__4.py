import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F

def test_bulk_update():
    # Create test users
    user1 = User.objects.create(username='user1', email='user1@example.com', first_name='John', last_name='Doe')
    user2 = User.objects.create(username='user2', email='user2@example.com', first_name='Jane', last_name='Doe')

    # Prepare update data
    user1.first_name = 'Johnny'
    user2.first_name = 'Janet'
    users = [user1, user2]

    # Test bulk_update with valid input
    assert User.objects.bulk_update(users, ['first_name']) == 2

    # Verify that users were updated
    assert User.objects.get(pk=user1.pk).first_name == 'Johnny'
    assert User.objects.get(pk=user2.pk).first_name == 'Janet'

    # Test bulk_update with a batch size
    assert User.objects.bulk_update(users, ['first_name'], batch_size=1) == 2
    
    # Test bulk_update with no fields
    with pytest.raises(ValueError, match='Field names must be given to bulk_update().'):
        User.objects.bulk_update(users, [])

    # Test bulk_update with None primary key
    user3 = User(username='user3', email='user3@example.com', first_name='Alice')
    with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
        User.objects.bulk_update([user3], ['first_name'])

    # Test bulk_update with primary key field
    user1.pk = None  # simulate no primary key
    with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
        User.objects.bulk_update(users, ['first_name', 'username'])