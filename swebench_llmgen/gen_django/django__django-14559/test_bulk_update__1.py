import copy
import operator
import warnings
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
from django.db.models.expressions import Case, Expression, F, Ref, Value, When
from django.db.models.functions import Cast, Trunc
from django.db.models.query_utils import FilteredRelation, Q
from django.db.models.sql.constants import CURSOR, GET_ITERATOR_CHUNK_SIZE
from django.db.models.utils import create_namedtuple_class, resolve_callables
from django.utils import timezone
from django.utils.functional import cached_property, partition
from django.contrib.auth.models import User
import pytest

def test_bulk_update():
    user1 = User.objects.create(username='user1', email='user1@example.com')
    user2 = User.objects.create(username='user2', email='user2@example.com')
    
    # Verify initial state
    assert user1.email == 'user1@example.com'
    assert user2.email == 'user2@example.com'
    
    # Update email addresses
    user1.email = 'new_user1@example.com'
    user2.email = 'new_user2@example.com'
    
    # Use bulk_update to apply changes
    User.objects.bulk_update([user1, user2], ['email'])
    
    # Refresh the users from the database
    user1.refresh_from_db()
    user2.refresh_from_db()
    
    # Verify updated state
    assert user1.email == 'new_user1@example.com'
    assert user2.email == 'new_user2@example.com'

def test_bulk_update_invalid_batch_size():
    user1 = User.objects.create(username='user1', email='user1@example.com')
    user2 = User.objects.create(username='user2', email='user2@example.com')
    
    # Attempting bulk_update with invalid batch size
    with pytest.raises(ValueError, match='Batch size must be a positive integer.'):
        User.objects.bulk_update([user1, user2], ['email'], batch_size=-1)

def test_bulk_update_no_fields():
    user1 = User.objects.create(username='user1', email='user1@example.com')
    
    # Attempting bulk_update with no fields
    with pytest.raises(ValueError, match='Field names must be given to bulk_update().'):
        User.objects.bulk_update([user1], [])

def test_bulk_update_without_primary_key():
    user = User(username='user1', email='user1@example.com')
    
    # Attempting bulk_update with objects that do not have a primary key
    with pytest.raises(ValueError, match='All bulk_update() objects must have a primary key set.'):
        User.objects.bulk_update([user], ['email'])

def test_bulk_update_with_primary_key_field():
    user1 = User.objects.create(username='user1', email='user1@example.com')
    
    # Attempting bulk_update with primary key field included
    with pytest.raises(ValueError, match='bulk_update() cannot be used with primary key fields.'):
        User.objects.bulk_update([user1], ['email', 'id'])