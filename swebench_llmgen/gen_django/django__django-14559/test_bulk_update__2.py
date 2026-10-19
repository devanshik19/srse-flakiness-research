import pytest
from django.contrib.auth.models import User
from django.db.models import F

@pytest.mark.django_db
def test_bulk_update_valid():
    # Create test users
    user1 = User.objects.create(username='testuser1', email='user1@example.com')
    user2 = User.objects.create(username='testuser2', email='user2@example.com')

    # Prepare updates
    users = [user1, user2]
    new_emails = ['new_user1@example.com', 'new_user2@example.com']
    
    # Perform bulk update
    User.objects.bulk_update(users, ['email'])

    # Refresh instances from database
    user1.refresh_from_db()
    user2.refresh_from_db()

    # Assert updates
    assert user1.email == 'user1@example.com'
    assert user2.email == 'user2@example.com'

@pytest.mark.django_db
def test_bulk_update_empty_fields():
    with pytest.raises(ValueError, match='Field names must be given to bulk_update().'):
        User.objects.bulk_update([], [])

@pytest.mark.django_db
def test_bulk_update_none_primary_key():
    user = User(username='testuser3')
    with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
        User.objects.bulk_update([user], ['email'])

@pytest.mark.django_db
def test_bulk_update_invalid_batch_size():
    user = User.objects.create(username='testuser4', email='user4@example.com')
    with pytest.raises(ValueError, match='Batch size must be a positive integer.'):
        User.objects.bulk_update([user], ['email'], batch_size=-1)

@pytest.mark.django_db
def test_bulk_update_with_primary_key_field():
    user = User.objects.create(username='testuser5', email='user5@example.com')
    with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
        User.objects.bulk_update([user], ['email', 'id'])

@pytest.mark.django_db
def test_bulk_update_with_m2m_field():
    user1 = User.objects.create(username='testuser6', email='user6@example.com')
    user2 = User.objects.create(username='testuser7', email='user7@example.com')
    with pytest.raises(ValueError, match='bulk_update() can only be used with concrete fields.'):
        User.objects.bulk_update([user1, user2], ['groups'])