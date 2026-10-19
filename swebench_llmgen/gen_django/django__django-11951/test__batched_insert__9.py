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
from django.db.models import QuerySet

def test_batched_insert():
    # Prepare the test data
    users = [User(username=f'user_{i}') for i in range(10)]
    queryset = User.objects
    
    # Test without ignore_conflicts
    inserted_rows = queryset._batched_insert(users, fields=['username'], batch_size=3, ignore_conflicts=False)
    
    # Verify users were inserted correctly
    assert len(inserted_rows) == 10
    assert all(User.objects.filter(username=user.username).exists() for user in users)

    # Test with ignore_conflicts when the database supports ignoring
    duplicate_user = User(username='duplicate_user')
    queryset._batched_insert([duplicate_user, duplicate_user], fields=['username'], batch_size=2, ignore_conflicts=True)

    # Assert only one duplicate is inserted when ignore_conflicts is True
    assert User.objects.filter(username='duplicate_user').count() == 1

    # Test with a database that does not support ignore_conflicts
    connections[settings.DATABASES['default']['ENGINE']].features.supports_ignore_conflicts = False
    with pytest.raises(NotSupportedError):
        queryset._batched_insert(users, fields=['username'], batch_size=3, ignore_conflicts=True)