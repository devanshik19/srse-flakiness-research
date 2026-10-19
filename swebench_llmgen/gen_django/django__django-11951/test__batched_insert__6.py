import copy
import operator
import warnings
from collections import namedtuple
from functools import lru_cache
from itertools import chain
from django.conf import settings
from django.core import exceptions
from django.db import (
    IntegrityError, connections, router,
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
from django.contrib.auth.models import User
import pytest

@pytest.mark.django_db
def test_batched_insert():
    # Create test data
    users = [User(username=f'user{i}') for i in range(10)]
    
    # Create QuerySet
    queryset = User.objects
    
    # Test without ignoring conflicts
    inserted_rows = queryset._batched_insert(users, fields=['username'], batch_size=3, ignore_conflicts=False)
    
    # Check the number of inserted rows
    assert len(inserted_rows) == 10
    assert User.objects.count() == 10

    # Test with ignore_conflicts set to True
    # First insert users for a second time to create conflicts
    queryset._batched_insert(users, fields=['username'], batch_size=3, ignore_conflicts=True)
    assert User.objects.count() == 10  # Ensure count remains the same due to conflict handling

    # Test with database that does not support ignore_conflicts
    with pytest.raises(NotSupportedError):
        with copy.deepcopy(connections) as mock_connections:
            mock_connections[queryset.db].features.supports_ignore_conflicts = False
            queryset._batched_insert(users, fields=['username'], batch_size=3, ignore_conflicts=True)