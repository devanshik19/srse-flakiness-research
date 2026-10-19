import copy
import operator
import warnings
from collections import namedtuple
from functools import lru_cache
from itertools import chain
from django.conf import settings
from django.core import exceptions
from django.db import IntegrityError, connections, router, transaction
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

@pytest.mark.parametrize("batch_size, ignore_conflicts, is_supported", [
    (1, False, True),
    (2, False, True),
    (1, True, True),
    (2, True, False),  # This case should raise NotSupportedError
])
def test_batched_insert(batch_size, ignore_conflicts, is_supported, db):
    queryset = User.objects.all()
    user_objs = [User(username=f'user{i}') for i in range(5)]
    
    if not is_supported and ignore_conflicts:
        with pytest.raises(NotSupportedError):
            queryset._batched_insert(user_objs, ['username'], batch_size, ignore_conflicts)
    else:
        inserted_rows = queryset._batched_insert(user_objs, ['username'], batch_size, ignore_conflicts)
        assert len(inserted_rows) == len(user_objs) if not ignore_conflicts else 0
        for i, row in enumerate(inserted_rows):
            assert row.username == f'user{i}'

@pytest.mark.parametrize("ignore_conflicts", [True, False])
def test_batched_insert_returning(ignore_conflicts, db):
    queryset = User.objects.all()
    user_objs = [User(username=f'user{i}') for i in range(3)]
    queryset._batched_insert(user_objs, ['username'], batch_size=None, ignore_conflicts=ignore_conflicts)
    
    all_users = User.objects.all()
    assert len(all_users) == len(user_objs)
    for i, user in enumerate(all_users):
        assert user.username == f'user{i}'