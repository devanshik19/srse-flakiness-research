import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F

@pytest.fixture
def user_factory():
    """Factory to create multiple User instances."""
    def create_users(num):
        return [User.objects.create(username=f"user{i}", email=f"user{i}@example.com") for i in range(num)]
    return create_users

def test_bulk_update(user_factory):
    # Create 5 users
    users = user_factory(5)

    # Prepare to update the email addresses
    for i, user in enumerate(users):
        user.email = f"updated_user{i}@example.com"

    # Perform bulk update
    updated_count = User.objects.bulk_update(users, ['email'])

    # Verify that the count of updated rows is correct
    assert updated_count == 5

    # Fetch updated users to confirm email changes
    for i, user in enumerate(users):
        updated_user = User.objects.get(pk=user.pk)
        assert updated_user.email == f"updated_user{i}@example.com"

def test_bulk_update_with_empty_fields(user_factory):
    users = user_factory(3)

    with pytest.raises(ValueError, match='Field names must be given to bulk_update().'):
        User.objects.bulk_update(users, [])

def test_bulk_update_with_none_primary_key(user_factory):
    users = user_factory(3)
    users[0].pk = None  # Simulate an object without a primary key

    with pytest.raises(ValueError, match='All bulk_update\\(\\) objects must have a primary key set.'):
        User.objects.bulk_update(users, ['email'])

def test_bulk_update_with_negative_batch_size(user_factory):
    users = user_factory(3)

    with pytest.raises(ValueError, match='Batch size must be a positive integer.'):
        User.objects.bulk_update(users, ['email'], batch_size=-1)

def test_bulk_update_with_primary_key_field(user_factory):
    users = user_factory(3)

    with pytest.raises(ValueError, match='bulk_update\\(\\) cannot be used with primary key fields.'):
        User.objects.bulk_update(users, ['email', 'id'])