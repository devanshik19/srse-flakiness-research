import copy
import operator
import warnings
from collections import namedtuple
from functools import lru_cache
from itertools import chain
import django
from django.conf import settings
from django.core import exceptions
from django.db import (
    DJANGO_VERSION_PICKLE_KEY, IntegrityError, NotSupportedError, connections,
    router, transaction,
)
from django.db.models import AutoField, DateField, DateTimeField, sql
from django.db.models.constants import LOOKUP_SEP
from django.db.models.deletion import Collector
from django.db.models.expressions import Case, Expression, F, Value, When
from django.db.models.functions import Cast, Trunc
from django.db.models.query_utils import FilteredRelation, Q
from django.db.models.sql.constants import CURSOR, GET_ITERATOR_CHUNK_SIZE
from django.db.models.utils import resolve_callables
from django.utils import timezone
from django.utils.functional import cached_property, partition
from django.contrib.auth.models import User
import pytest

def test_query():
    user = User.objects.create_user(username='testuser', password='testpass')

    queryset = User.objects.filter(username='testuser')

    # Accessing query before setting deferred_filter
    assert queryset.query() is not None

    # Set a deferred filter
    queryset._deferred_filter = (False, ('username',), {})
    
    # Check that deferred_filter is applied
    assert queryset.query() is not None
    assert queryset.first() == user

    # Clear the deferred_filter
    queryset.query()
    assert queryset._deferred_filter is None

    # Verify that the query still returns user.
    assert queryset.first() == user

    # Assert that accessing query again does not alter _deferred_filter
    initial_deferred_filter = queryset._deferred_filter
    queryset.query()
    assert queryset._deferred_filter == initial_deferred_filter