import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import QuerySet

@pytest.mark.django_db
def test_bulk_update():
    # Create test users
    user1 = User.objects.create(username='user1', email='user1@example.com')
    user2 = User.objects.create(username='user2', email='user2@example.com')
    
    # Prepare update fields
    users = [user1, user2]
    fields = ['email']
    
    # Update emails
    new_emails = ['new_user1@example.com', 'new_user2@example.com']
    for user, new_email in zip(users, new_emails):
        user.email = new_email
    
    # Perform bulk update
    queryset = User.objects
    rows_updated = queryset.bulk_update(users, fields)
    
    # Assert that two rows were updated
    assert rows_updated == 2
    
    # Verify the updates in the database
    user1.refresh_from_db()
    user2.refresh_from_db()
    assert user1.email == 'new_user1@example.com'
    assert user2.email == 'new_user2@example.com'

def test_bulk_update_invalid_batch_size():
    user = User.objects.create(username='user3', email='user3@example.com')
    with pytest.raises(ValueError, match='Batch size must be a positive integer.'):
        User.objects.bulk_update([user], ['email'], batch_size=-1)

def test_bulk_update_no_fields():
    user = User.objects.create(username='user4', email='user4@example.com')
    with pytest.raises(ValueError, match='Field names must be given to bulk_update().'):
        User.objects.bulk_update([user], [])

def test_bulk_update_pk_not_set():
    user = User(username='user5', email='user5@example.com')
    with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
        User.objects.bulk_update([user], ['email'])

def test_bulk_update_with_non_concrete_field():
    class NonConcreteUser(User):
        pass
    non_concrete_user = NonConcreteUser(username='user6', email='user6@example.com')
    with pytest.raises(ValueError, match='bulk_update() can only be used with concrete fields.'):
        User.objects.bulk_update([non_concrete_user], ['username'])

def test_bulk_update_with_primary_key_field():
    user = User.objects.create(username='user7', email='user7@example.com')
    with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
        User.objects.bulk_update([user], ['id'])