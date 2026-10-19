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
import pytest
from django.contrib.auth.models import User
from django.db.models.query import QuerySet


def test_batched_insert():
    # Prepare test data
    users = [User(username=f'user{i}') for i in range(10)]  # Create 10 user instances

    qs = User.objects  # Get the queryset for User model

    # Test without ignore_conflicts
    inserted_users = qs._batched_insert(users, fields=['username'], batch_size=5, ignore_conflicts=False)

    assert len(inserted_users) == 10
    assert all(user.username.startswith('user') for user in inserted_users)
    
    # Verify the entries in the database
    assert User.objects.count() == 10  # Expecting 10 users created

    # Test with ignore_conflicts (for simplicity we can assume no conflict)
    user_conflict = User(username='user1')  # User with a username that would cause a conflict
    users_with_conflict = users + [user_conflict]

    inserted_users_conflict = qs._batched_insert(users_with_conflict, fields=['username'], batch_size=5, ignore_conflicts=True)

    assert len(inserted_users_conflict) == 10  # Still expecting 10 as 'ignore_conflicts' is set to True
    
    # Ensure we didn't insert the conflicting username
    assert User.objects.count() == 10  # Still 10 users in the database

    # Now we will force an error by attempting to ignore conflicts on a DB that doesn't support it
    with pytest.raises(NotSupportedError):
        qs._batched_insert(users, fields=['username'], batch_size=5, ignore_conflicts=True)