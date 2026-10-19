import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F

@pytest.mark.django_db
def test_bulk_update():
    # Create sample users
    user1 = User.objects.create(username='user1', email='user1@example.com')
    user2 = User.objects.create(username='user2', email='user2@example.com')
    user3 = User.objects.create(username='user3', email='user3@example.com')

    # Prepare objects to update
    user1.email = 'new_email1@example.com'
    user2.email = 'new_email2@example.com'
    user3.email = 'new_email3@example.com'
    
    # Perform bulk update
    queryset = User.objects
    rows_updated = queryset.bulk_update([user1, user2, user3], ['email'])

    # Verify the return value
    assert rows_updated == 3

    # Reload users and verify the fields were updated
    user1.refresh_from_db()
    user2.refresh_from_db()
    user3.refresh_from_db()
    
    assert user1.email == 'new_email1@example.com'
    assert user2.email == 'new_email2@example.com'
    assert user3.email == 'new_email3@example.com'

def test_bulk_update_with_invalid_batch_size():
    user1 = User.objects.create(username='user4', email='user4@example.com')
    user2 = User.objects.create(username='user5', email='user5@example.com')

    queryset = User.objects

    with pytest.raises(ValueError, match='Batch size must be a positive integer.'):
        queryset.bulk_update([user1, user2], ['email'], batch_size=-1)

def test_bulk_update_with_empty_fields():
    user1 = User.objects.create(username='user6', email='user6@example.com')
    user2 = User.objects.create(username='user7', email='user7@example.com')

    queryset = User.objects

    with pytest.raises(ValueError, match='Field names must be given to bulk_update().'):
        queryset.bulk_update([user1, user2], [])

def test_bulk_update_with_none_pk():
    user1 = User(username='user8', email='user8@example.com')

    queryset = User.objects

    with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
        queryset.bulk_update([user1], ['email'])

def test_bulk_update_with_primary_key_field():
    user1 = User.objects.create(username='user9', email='user9@example.com')

    queryset = User.objects

    with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
        queryset.bulk_update([user1], ['username'])