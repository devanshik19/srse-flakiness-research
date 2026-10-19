import pytest
from django.contrib.auth.models import User
from django.db import transaction

@pytest.mark.django_db
def test_bulk_update():
    # Create users to be updated
    user1 = User.objects.create(username='user1', email='user1@example.com')
    user2 = User.objects.create(username='user2', email='user2@example.com')
    user3 = User.objects.create(username='user3', email='user3@example.com')

    # List of users to update
    users_to_update = [user1, user2, user3]
    
    # Define fields to update
    fields_to_update = ['email']

    # Perform bulk update
    updated_count = User.objects.bulk_update(users_to_update, fields_to_update)

    # Validate updates
    assert updated_count == 3
    assert User.objects.get(pk=user1.pk).email == 'user1@example.com'
    assert User.objects.get(pk=user2.pk).email == 'user2@example.com'
    assert User.objects.get(pk=user3.pk).email == 'user3@example.com'

    # Test with invalid batch size
    with pytest.raises(ValueError, match='Batch size must be a positive integer.'):
        User.objects.bulk_update(users_to_update, fields_to_update, batch_size=-1)

    # Test without fields
    with pytest.raises(ValueError, match='Field names must be given to bulk_update().'):
        User.objects.bulk_update(users_to_update, [])

    # Test with objects missing primary keys
    user_no_pk = User(username='user4', email='user4@example.com')
    with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
        User.objects.bulk_update([user_no_pk], fields_to_update)

    # Test with non-concrete field (Not applicable in this example but kept for completeness)
    # Assuming some other model with a M2M field which we don't have here; left as an example only
    # with pytest.raises(ValueError, match='bulk_update() can only be used with concrete fields.'):
    #     SomeModel.objects.bulk_update([...], [...])

    # Test with primary key field (Not applicable here since we update 'email')
    # with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
    #     User.objects.bulk_update(users_to_update, ['id'])  # Using 'id', which is a primary key