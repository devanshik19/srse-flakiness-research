import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.query import QuerySet

# Creating a custom QuerySet to test bulk_update method
class CustomQuerySet(QuerySet):
    pass

@pytest.mark.django_db
def test_bulk_update():
    # Create a few User objects
    user1 = User.objects.create(username='user1', email='user1@example.com')
    user2 = User.objects.create(username='user2', email='user2@example.com')
    
    # Prepare the users list for bulk_update
    users_to_update = [user1, user2]
    
    # Fields we want to update
    fields_to_update = ['email']

    # Update user emails via bulk_update
    user1.email = 'new_user1@example.com'
    user2.email = 'new_user2@example.com'
    updated_count = CustomQuerySet(User).bulk_update(users_to_update, fields_to_update)

    # Refresh the users from the database
    user1.refresh_from_db()
    user2.refresh_from_db()

    # Assertions to ensure emails are updated correctly
    assert updated_count == 2
    assert user1.email == 'new_user1@example.com'
    assert user2.email == 'new_user2@example.com'

def test_bulk_update_empty_fields():
    with pytest.raises(ValueError, match='Field names must be given to bulk_update().'):
        CustomQuerySet(User).bulk_update([], [])

def test_bulk_update_no_primary_key():
    user = User(username='user3', email='user3@example.com')
    with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
        CustomQuerySet(User).bulk_update([user], ['email'])

def test_bulk_update_negative_batch_size():
    with pytest.raises(ValueError, match='Batch size must be a positive integer.'):
        CustomQuerySet(User).bulk_update([], ['email'], batch_size=-1)

def test_bulk_update_with_many_to_many_field():
    user1 = User.objects.create(username='user4', email='user4@example.com')
    # Assume there's a M2M field 'groups' set up, we raise ValueError
    with pytest.raises(ValueError, match='bulk_update() can only be used with concrete fields.'):
        CustomQuerySet(User).bulk_update([user1], ['groups'])