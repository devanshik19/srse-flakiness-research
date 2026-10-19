import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F

@pytest.mark.parametrize("batch_size, expected", [
    (None, 2),
    (1, 1),
    (3, 2),
])
def test_bulk_update(batch_size, expected):
    # Create test users
    user1 = User.objects.create(username='user1', email='user1@example.com')
    user2 = User.objects.create(username='user2', email='user2@example.com')
    users = [user1, user2]

    # Update email for both users
    for user in users:
        user.email = 'updated_' + user.email
    User.objects.bulk_update(users, ['email'], batch_size=batch_size)

    # Refresh users from the database
    user1.refresh_from_db()
    user2.refresh_from_db()

    # Assertions
    assert user1.email == 'updated_user1@example.com'
    assert user2.email == 'updated_user2@example.com'


def test_bulk_update_no_primary_key():
    user = User(username='user3')
    
    with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
        User.objects.bulk_update([user], ['email'])

        
def test_bulk_update_empty_fields():
    user1 = User.objects.create(username='user4', email='user4@example.com')

    with pytest.raises(ValueError, match='Field names must be given to bulk_update().'):
        User.objects.bulk_update([user1], [])
        

def test_bulk_update_with_non_concrete_field():
    user1 = User.objects.create(username='user5', email='user5@example.com')
    
    with pytest.raises(ValueError, match='bulk_update() can only be used with concrete fields.'):
        User.objects.bulk_update([user1], ['date_joined'])  # date_joined is a non-concrete field
        

def test_bulk_update_with_primary_key_field():
    user1 = User.objects.create(username='user6', email='user6@example.com')
    
    with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
        User.objects.bulk_update([user1], ['id'])