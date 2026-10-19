import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import QuerySet

@pytest.fixture
def user_queryset():
    return User.objects.all()

def test_bulk_create_valid(user_queryset):
    users = [User(username=f'user{i}', email=f'user{i}@example.com') for i in range(5)]
    created_users = user_queryset.bulk_create(users)

    assert len(created_users) == 5
    assert all(isinstance(user, User) for user in created_users)
    assert all(user.pk is not None for user in created_users)

def test_bulk_create_empty_list(user_queryset):
    created_users = user_queryset.bulk_create([])

    assert created_users == []

def test_bulk_create_with_batch_size(user_queryset):
    users = [User(username=f'user{i}', email=f'user{i}@example.com') for i in range(5)]
    created_users = user_queryset.bulk_create(users, batch_size=2)

    assert len(created_users) == 5
    assert all(isinstance(user, User) for user in created_users)

def test_bulk_create_invalid_batch_size(user_queryset):
    with pytest.raises(ValueError, match="Batch size must be a positive integer."):
        user_queryset.bulk_create([], batch_size=0)

def test_bulk_create_unique_constraint(user_queryset):
    users = [User(username='duplicate_user', email=f'user{i}@example.com') for i in range(5)]
    
    # Assuming some state to force a unique conflict to test ignore and update options
    User.objects.create(username='duplicate_user', email='existing@example.com')
    
    created_users = user_queryset.bulk_create(users, ignore_conflicts=True)

    assert len(created_users) == 5
    assert User.objects.filter(username='duplicate_user').count() == 1

def test_bulk_create_multi_table_inheritance(user_queryset):
    # Testing multi-table inheritance by attempting to bulk create a User instance
    # Expecting a ValueError
    class Admin(User):
        class Meta:
            db_table = 'auth_user'

    with pytest.raises(ValueError, match="Can't bulk create a multi-table inherited model"):
        user_queryset.bulk_create([Admin(username='admin_user', email='admin@example.com')])