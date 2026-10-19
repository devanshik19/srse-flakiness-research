import copy
import operator
import warnings
from collections import namedtuple
from functools import lru_cache
from itertools import chain
from django.conf import settings
from django.core import exceptions
from django.db import (
    IntegrityError, connections, transaction,
)
from django.db.models import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User

def test_batched_insert_ignore_conflicts():
    # Create a queryset with some User instances
    users = [User(username=f'user{i}') for i in range(5)]
    User.objects.bulk_create(users)

    queryset = User.objects

    # Assuming the database supports ignore conflicts
    try:
        # Batch insert with ignore_conflicts set to True
        inserted_rows = queryset._batched_insert(users, ['username'], batch_size=2, ignore_conflicts=True)
        assert len(inserted_rows) == 0  # No new rows should be inserted, as they already exist
    except NotSupportedError:
        pass  # Database doesn't support ignore conflicts

def test_batched_insert_without_ignore_conflicts():
    # Create new User instances
    users = [User(username=f'user_new{i}') for i in range(5)]
    
    # Create a queryset
    queryset = User.objects

    # Batch insert without ignore_conflicts
    inserted_rows = queryset._batched_insert(users, ['username'], batch_size=2, ignore_conflicts=False)
    assert len(inserted_rows) == len(users)  # All new users should be inserted

    for user in inserted_rows:
        assert User.objects.filter(username=user.username).exists()  # Verify inserted rows exist in DB

def test_batched_insert_with_non_existing_batch():
    # Create a queryset
    queryset = User.objects

    # Try inserting no user
    inserted_rows = queryset._batched_insert([], ['username'], batch_size=2, ignore_conflicts=False)
    assert inserted_rows == []  # No rows should be returned for an empty input list

def test_batched_insert_large_batch():
    # Create a queryset
    queryset = User.objects

    # Create a large number of new User instances
    users = [User(username=f'user_batch{i}') for i in range(100)]

    # Batch insert with larger batch size
    inserted_rows = queryset._batched_insert(users, ['username'], batch_size=50, ignore_conflicts=False)
    assert len(inserted_rows) == len(users)  # All new users should be inserted

    for user in inserted_rows:
        assert User.objects.filter(username=user.username).exists()  # Verify inserted rows exist in DB