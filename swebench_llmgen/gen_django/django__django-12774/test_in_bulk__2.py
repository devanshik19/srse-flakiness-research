import copy
import operator
import warnings
from collections import namedtuple
from functools import lru_cache
from itertools import chain
from django.conf import settings
from django.core import exceptions
from django.db import (
    IntegrityError, NotSupportedError, connections,
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
from django.utils.version import get_version
from django.contrib.auth.models import User
import pytest

# Test cases for in_bulk method
def test_in_bulk_with_id_list():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user3 = User.objects.create(username='user3')

    id_list = [user1.id, user2.id]
    results = User.objects.in_bulk(id_list)

    assert results[user1.id] == user1
    assert results[user2.id] == user2
    assert user3.id not in results

def test_in_bulk_with_empty_id_list():
    results = User.objects.in_bulk(id_list=[])
    assert results == {}

def test_in_bulk_with_none_id_list():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    results = User.objects.in_bulk()
    assert results[user1.id] == user1
    assert results[user2.id] == user2

def test_in_bulk_with_field_name():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user3 = User.objects.create(username='user3')

    id_list = [user1.username, user2.username]
    results = User.objects.in_bulk(id_list, field_name='username')

    assert results[user1.username] == user1
    assert results[user2.username] == user2
    assert user3.username not in results

def test_in_bulk_with_invalid_field_name():
    user = User.objects.create(username='user1')

    with pytest.raises(ValueError):
        User.objects.in_bulk(id_list=[user.id], field_name='invalid_field')

def test_in_bulk_with_slicing():
    with pytest.raises(AssertionError):
        User.objects.all()[:10].in_bulk()