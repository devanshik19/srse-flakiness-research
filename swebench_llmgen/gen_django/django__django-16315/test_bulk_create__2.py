import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError

from django.db.models import QuerySet

@pytest.fixture
def user_queryset():
    return User.objects.none()  # Start with an empty queryset

def test_bulk_create_valid(user_queryset):
    # Prepare user instances to bulk create
    users = [
        User(username='user1', email='user1@example.com'),
        User(username='user2', email='user2@example.com'),
        User(username='user3', email='user3@example.com')
    ]

    created_users = user_queryset.bulk_create(users)
    
    # Verify the users are created
    assert len(created_users) == 3
    assert User.objects.filter(username='user1').exists()
    assert User.objects.filter(username='user2').exists()
    assert User.objects.filter(username='user3').exists()

def test_bulk_create_empty(user_queryset):
    # Test with an empty list
    created_users = user_queryset.bulk_create([])
    
    assert created_users == []

def test_bulk_create_conflict(user_queryset):
    # Create a user first
    User.objects.create(username='user1', email='user1@example.com')

    users_with_conflict = [
        User(username='user1', email='user1@example.com'),  # Conflict
        User(username='user2', email='user2@example.com')
    ]

    # Attempting to bulk create with ignore_conflicts=True
    created_users = user_queryset.bulk_create(users_with_conflict, ignore_conflicts=True)

    assert len(created_users) == 2
    assert User.objects.filter(username='user1').count() == 1  # Original should remain
    assert User.objects.filter(username='user2').exists()

def test_bulk_create_invalid_batch_size(user_queryset):
    users = [
        User(username='user1', email='user1@example.com')
    ]
    with pytest.raises(ValueError, match="Batch size must be a positive integer."):
        user_queryset.bulk_create(users, batch_size=0)

    with pytest.raises(ValueError, match="Batch size must be a positive integer."):
        user_queryset.bulk_create(users, batch_size=-1)

def test_bulk_create_multi_table_inheritance(user_queryset):
    # Prepare user instances with a hypothetical multi-table inheritance situation
    # Assuming there is such a condition in the model for demonstration.
    class MultiTableUser(User):
        class Meta:
            proxy = True
            
    users = [
        MultiTableUser(username='user1', email='user1@example.com'),
        MultiTableUser(username='user2', email='user2@example.com'),
    ]

    with pytest.raises(ValueError, match="Can't bulk create a multi-table inherited model"):
        user_queryset.bulk_create(users)