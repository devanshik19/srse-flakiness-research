import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.db.utils import NotSupportedError
from django.db.models import QuerySet


def test_batched_insert_with_ignore_conflicts():
    qs = User.objects
    users = [User(username=f'user{i}') for i in range(10)]
    
    # Create with ignore_conflicts = True
    qs._batched_insert(users, fields=['username'], batch_size=5, ignore_conflicts=True)

    assert User.objects.count() == 10  # All users should be inserted


def test_batched_insert_without_ignore_conflicts():
    qs = User.objects
    users = [User(username=f'user{i}') for i in range(10)]
    
    # Insert users
    qs._batched_insert(users, fields=['username'], batch_size=5, ignore_conflicts=False)

    assert User.objects.count() == 10  # All users should be inserted


def test_batched_insert_when_not_supported_ignore_conflicts():
    qs = User.objects
    users = [User(username=f'user{i}') for i in range(5)]

    # Testing NotSupportedError
    with pytest.raises(NotSupportedError):
        qs._batched_insert(users, fields=['username'], batch_size=5, ignore_conflicts=True)


def test_batched_insert_with_batch_size():
    qs = User.objects
    users = [User(username=f'user{i}') for i in range(10)]

    # Insert with a batch size of 3
    qs._batched_insert(users, fields=['username'], batch_size=3, ignore_conflicts=False)

    assert User.objects.count() == 10  # All users should be inserted