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

class QuerySetTest:
    @pytest.fixture
    def setup_users(self):
        users = [User(username=f'user{i}', password='password') for i in range(10)]
        User.objects.bulk_create(users)
        return users

    def test_batched_insert_without_conflicts(self, setup_users):
        existing_user_count = User.objects.count()
        users_to_insert = [User(username=f'new_user{i}', password='password') for i in range(5)]
        qs = User.objects

        inserted_rows = qs._batched_insert(users_to_insert, fields=['username', 'password'], batch_size=2, ignore_conflicts=False)

        assert User.objects.count() == existing_user_count + len(users_to_insert)
        assert len(inserted_rows) == len(users_to_insert)

    def test_batched_insert_with_conflicts(self, setup_users):
        users_to_insert = [User(username='user0', password='new_password'), 
                           User(username='user1', password='new_password')]
        qs = User.objects

        with pytest.raises(NotSupportedError):
            qs._batched_insert(users_to_insert, fields=['username', 'password'], batch_size=2, ignore_conflicts=True)

    def test_batched_insert_large_batch(self, setup_users):
        existing_user_count = User.objects.count()
        users_to_insert = [User(username=f'new_user{i}', password='password') for i in range(20)]
        qs = User.objects
        
        inserted_rows = qs._batched_insert(users_to_insert, fields=['username', 'password'], batch_size=10, ignore_conflicts=False)

        assert User.objects.count() == existing_user_count + len(users_to_insert)
        assert len(inserted_rows) == len(users_to_insert)

    def test_batched_insert_with_ignore_conflicts(self, setup_users):
        users_to_insert = [User(username='user0', password='new_password'), 
                           User(username='user2', password='new_password')]
        qs = User.objects

        inserted_rows = qs._batched_insert(users_to_insert, fields=['username', 'password'], batch_size=1, ignore_conflicts=True)

        assert User.objects.count() == len(setup_users) + 1
        assert len(inserted_rows) == 1  # Only one row should be inserted