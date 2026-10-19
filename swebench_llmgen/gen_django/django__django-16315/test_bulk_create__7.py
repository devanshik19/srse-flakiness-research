import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError

@pytest.fixture
def user_instances():
    return [
        User(username='user1', email='user1@example.com'),
        User(username='user2', email='user2@example.com'),
    ]

def test_bulk_create_success(user_instances):
    qs = User.objects.bulk_create(user_instances)
    assert len(qs) == len(user_instances)
    assert User.objects.count() == 2

def test_bulk_create_empty_list():
    qs = User.objects.bulk_create([])
    assert qs == []

def test_bulk_create_batch_size(user_instances):
    qs = User.objects.bulk_create(user_instances, batch_size=1)
    assert len(qs) == len(user_instances)
    assert User.objects.count() == 2

def test_bulk_create_invalid_batch_size():
    with pytest.raises(ValueError, match="Batch size must be a positive integer."):
        User.objects.bulk_create(user_instances, batch_size=0)

def test_bulk_create_unique_constraint(user_instances):
    User.objects.bulk_create(user_instances)
    with pytest.raises(IntegrityError):
        User.objects.bulk_create([User(username='user1', email='user1@example.com')])

def test_bulk_create_ignore_conflicts(user_instances):
    User.objects.bulk_create(user_instances)
    qs = User.objects.bulk_create([User(username='user1', email='new_email@example.com')], ignore_conflicts=True)
    assert len(qs) == 0
    assert User.objects.count() == 2

def test_bulk_create_update_conflicts(user_instances):
    User.objects.bulk_create(user_instances)
    User.objects.bulk_create(
        [User(username='user1', email='updated_email@example.com')],
        update_conflicts=True,
        unique_fields=['username']
    )
    user = User.objects.get(username='user1')
    assert user.email == 'updated_email@example.com'