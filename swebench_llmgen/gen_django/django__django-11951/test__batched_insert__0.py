import copy
import operator
import warnings
from collections import namedtuple
from functools import lru_cache
from itertools import chain
from django.conf import settings
from django.core import exceptions
from django.db import (
    DJANGO_VERSION_PICKLE_KEY, IntegrityError, connections, router,
    transaction,
)
from django.db.models import DateField, DateTimeField, sql
from django.db.models.constants import LOOKUP_SEP
from django.db.models.deletion import Collector
from django.db.models.expressions import Case, Expression, F, Value, When
from django.db.models.fields import AutoField
from django.db.models.functions import Cast, Trunc
from django.db.models.query_utils import FilteredRelation, InvalidQuery, Q
from django.db.models.sql.constants import CURSOR, GET_ITERATOR_CHUNK_SIZE
from django.db.utils import NotSupportedError
from django.utils import timezone
from django.utils.functional import cached_property, partition
from django.utils.version import get_version
import pytest
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

def test_batched_insert():
    # Create a queryset for User model
    qs = User.objects.all()
    
    # Prepare test data
    users_to_insert = [
        User(username=f'user{i}', password='password') for i in range(10)
    ]

    # Use _batched_insert to insert users in batches of 3
    inserted_rows = qs._batched_insert(users_to_insert, fields=['username', 'password'], batch_size=3, ignore_conflicts=False)

    # Ensure we have the right number of inserted rows
    assert len(inserted_rows) == 10  # Expecting all 10 users to be inserted
    assert User.objects.count() == 10  # Check if database reflects the insertion

    # Test insertion with ignore_conflicts=True 
    users_conflict = [
        User(username='user0', password='new_password')  # This will conflict
    ]

    with pytest.raises(NotSupportedError):
        # Expect NotSupportedError due to database backend not supporting ignoring conflicts
        qs._batched_insert(users_conflict, fields=['username', 'password'], batch_size=3, ignore_conflicts=True)

    # Testing insertion with ignoring conflicts where supported
    # Let's use different usernames
    users_ignore_conflict = [
        User(username='user10', password='password'),  # New user, no conflict
        User(username='user11', password='password'),  # New user, no conflict
    ]
    
    inserted_rows_ignore = qs._batched_insert(users_ignore_conflict, fields=['username', 'password'], batch_size=3, ignore_conflicts=False)

    # Expect 2 new users to be inserted
    assert len(inserted_rows_ignore) == 2
    assert User.objects.count() == 12  # Expecting total count now is 12