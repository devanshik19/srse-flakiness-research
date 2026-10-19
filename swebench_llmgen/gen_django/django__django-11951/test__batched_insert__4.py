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
from django.contrib.auth.models import User
import pytest

def test_batched_insert():
    batch_size = 2
    users = [User(username=f'user{i}') for i in range(5)]
    
    qs = User.objects
    
    # Inserting users without ignoring conflicts
    inserted_users = qs._batched_insert(users, fields=['username'], batch_size=batch_size)
    
    assert len(inserted_users) == len(users)
    assert all(User.objects.filter(username=user.username).exists() for user in users)

    # Test with ignore_conflicts set to True
    existing_user = User(username='conflict_user')
    existing_user.save()
    users_conflict = [existing_user] + users  # This will cause a conflict
    
    inserted_users_with_conflict = qs._batched_insert(users_conflict, fields=['username'], batch_size=batch_size, ignore_conflicts=True)
    
    assert len(inserted_users_with_conflict) == batch_size  # Only the first batch should be inserted
    assert User.objects.count() == (len(users) + 1)  # Existing user should remain, new users added
    assert User.objects.filter(username='conflict_user').count() == 1  # No duplicate

    # Test NotSupportedError
    with pytest.raises(NotSupportedError):
        qs._batched_insert(users, fields=['username'], batch_size=batch_size, ignore_conflicts=True)