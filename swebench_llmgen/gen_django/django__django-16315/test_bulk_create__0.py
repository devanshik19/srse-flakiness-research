import copy
import operator
import warnings
from itertools import chain, islice
from asgiref.sync import sync_to_async
import django
from django.conf import settings
from django.core import exceptions
from django.db import (
    DJANGO_VERSION_PICKLE_KEY,
    IntegrityError,
    NotSupportedError,
    connections,
    router,
    transaction,
)
from django.db.models import AutoField
from django.db.models import QuerySet
from django.contrib.auth.models import User
import pytest

@pytest.fixture
def user_objects():
    return [User(username=f'user{i}') for i in range(5)]

def test_bulk_create_success(user_objects):
    queryset = User.objects
    created_users = queryset.bulk_create(user_objects)

    assert len(created_users) == 5
    for user in created_users:
        assert User.objects.filter(username=user.username).exists()

def test_bulk_create_empty(user_objects):
    queryset = User.objects
    created_users = queryset.bulk_create([])

    assert created_users == []

def test_bulk_create_with_batch_size(user_objects):
    queryset = User.objects
    created_users = queryset.bulk_create(user_objects, batch_size=2)

    assert len(created_users) == 5
    for user in created_users:
        assert User.objects.filter(username=user.username).exists()

def test_bulk_create_invalid_batch_size(user_objects):
    queryset = User.objects

    with pytest.raises(ValueError, match="Batch size must be a positive integer."):
        queryset.bulk_create(user_objects, batch_size=0)

def test_bulk_create_with_ignore_conflicts(user_objects):
    queryset = User.objects
    queryset.bulk_create(user_objects)
    
    # Attempt to create users with the same username but ignore conflicts
    conflicted_users = [User(username=f'user{i}') for i in range(3)]
    created_users = queryset.bulk_create(conflicted_users, ignore_conflicts=True)

    assert len(created_users) == 3  # Those that didn't conflict should be inserted
    for user in created_users:
        assert User.objects.filter(username=user.username).exists()

def test_bulk_create_multi_table_inheritance(user_objects):
    queryset = User.objects

    with pytest.raises(ValueError, match="Can't bulk create a multi-table inherited model"):
        queryset.bulk_create(user_objects + user_objects)  # Simulate multi-table by duplicating objects