import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F

@pytest.mark.django_db
def test_bulk_update():
    # Create test users
    user1 = User.objects.create(username='user1', email='user1@example.com', first_name='First', last_name='User')
    user2 = User.objects.create(username='user2', email='user2@example.com', first_name='Second', last_name='User')
    
    # Prepare the objects to be updated
    user1.first_name = 'First Updated'
    user2.first_name = 'Second Updated'
    
    # Test bulk update with valid fields
    queryset = User.objects.all()
    updated_count = queryset.bulk_update([user1, user2], ['first_name'])
    
    assert updated_count == 2
    assert User.objects.get(pk=user1.pk).first_name == 'First Updated'
    assert User.objects.get(pk=user2.pk).first_name == 'Second Updated'
    
    # Test bulk update with batch_size
    user1.last_name = 'User One'
    user2.last_name = 'User Two'
    updated_count = queryset.bulk_update([user1, user2], ['last_name'], batch_size=1)
    
    assert updated_count == 2
    assert User.objects.get(pk=user1.pk).last_name == 'User One'
    assert User.objects.get(pk=user2.pk).last_name == 'User Two'
    
    # Test bulk update with no fields
    with pytest.raises(ValueError, match='Field names must be given to bulk_update().'):
        queryset.bulk_update([user1, user2], [])

    # Test bulk update with None primary key
    user3 = User(username='user3', email='user3@example.com', first_name='Third')
    with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
        queryset.bulk_update([user3], ['first_name'])

    # Test bulk update with non-concrete field
    user1.is_active = False
    user2.is_active = True
    with pytest.raises(ValueError, match='bulk_update() can only be used with concrete fields.'):
        queryset.bulk_update([user1, user2], ['is_active'])

    # Test bulk update with primary key in fields
    user1.pk = None  # This should not happen in a regular update
    user2.username = 'user2_updated'
    with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
        queryset.bulk_update([user1, user2], ['username', 'pk'])