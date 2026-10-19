import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F

@pytest.mark.django_db
def test_bulk_update():
    # Create 5 user instances
    users = [
        User.objects.create(username=f'user{i}', email=f'user{i}@example.com') for i in range(5)
    ]

    # Update fields for bulk_update
    for user in users:
        user.first_name = f'FirstName{user.id}'
        user.last_name = f'LastName{user.id}'

    # Use bulk_update to update first_name and last_name
    rows_updated = User.objects.bulk_update(users, ['first_name', 'last_name'], batch_size=2)

    # Verify the number of rows updated
    assert rows_updated == 5

    # Verify the changes were applied correctly
    for user in users:
        updated_user = User.objects.get(pk=user.pk)
        assert updated_user.first_name == f'FirstName{user.id}'
        assert updated_user.last_name == f'LastName{user.id}'

def test_bulk_update_with_empty_fields():
    users = [
        User.objects.create(username=f'user{i}', email=f'user{i}@example.com') for i in range(3)
    ]

    with pytest.raises(ValueError, match='Field names must be given to bulk_update()'):
        User.objects.bulk_update(users, [])

def test_bulk_update_with_none_primary_key():
    user = User.objects.create(username='user', email='user@example.com')
    user.pk = None  # Remove primary key

    with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
        User.objects.bulk_update([user], ['first_name'])

def test_bulk_update_with_non_concrete_field():
    user = User.objects.create(username='user', email='user@example.com')

    with pytest.raises(ValueError, match='bulk_update() can only be used with concrete fields.'):
        User.objects.bulk_update([user], ['date_joined'])

def test_bulk_update_with_primary_key_field():
    user = User.objects.create(username='user', email='user@example.com')

    with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
        User.objects.bulk_update([user], ['pk'])

def test_bulk_update_with_negative_batch_size():
    users = [
        User.objects.create(username=f'user{i}', email=f'user{i}@example.com') for i in range(2)
    ]

    with pytest.raises(ValueError, match='Batch size must be a positive integer.'):
        User.objects.bulk_update(users, ['first_name'], batch_size=-1)