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
from django.db.models import QuerySet


def test_batched_insert(db):
    # Test data preparation
    users = [User(username=f'user{i}') for i in range(10)]
    
    # Create a QuerySet for bulk inserting
    queryset = User.objects
    
    # Invoke _batched_insert method directly
    inserted_users = queryset._batched_insert(users, ['username'], batch_size=3, ignore_conflicts=False)
    
    # Assert all users are inserted
    assert len(inserted_users) == 10
    assert all(user.username.startswith('user') for user in inserted_users)
    
    # Test ignoring conflicts with ignore_conflicts=True
    existing_user = User.objects.create(username='existing_user')
    users_with_conflict = [User(username='existing_user')] + users
    
    with pytest.raises(NotSupportedError):
        queryset._batched_insert(users_with_conflict, ['username'], batch_size=3, ignore_conflicts=True)

    # Now test with a supported backend
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Assume ignore_conflicts is supported (this normally depends on the database)
        inserted_users_conflict = queryset._batched_insert(users_with_conflict, ['username'], batch_size=3, ignore_conflicts=True)
        
        # Assert only new users are inserted
        assert len(inserted_users_conflict) == 10  # existing_user will be ignored
        assert all(user.username.startswith('user') for user in inserted_users_conflict)
        
        # Assert that warnings are generated if any
        assert len(w) > 0