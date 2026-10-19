import difflib
import functools
import inspect
import sys
import warnings
from collections import Counter, namedtuple
from collections.abc import Iterator, Mapping
from itertools import chain, count, product
from string import ascii_uppercase
from django.core.exceptions import EmptyResultSet, FieldDoesNotExist, FieldError
from django.db import DEFAULT_DB_ALIAS, NotSupportedError, connections
from django.db.models.aggregates import Count
from django.db.models.constants import LOOKUP_SEP
from django.db.models.expressions import BaseExpression, Col, F, OuterRef, Ref, SimpleCol
from django.db.models.fields import Field
from django.db.models.fields.related_lookups import MultiColSource
from django.db.models.lookups import Lookup
from django.db.models.query_utils import Q, check_rel_lookup_compatibility, refs_expression
from django.db.models.sql.constants import INNER, LOUTER, ORDER_DIR, ORDER_PATTERN, SINGLE
from django.db.models.sql.datastructures import BaseTable, Empty, Join, MultiJoin
from django.db.models.sql.where import AND, OR, ExtraWhere, NothingNode, WhereNode
from django.utils.deprecation import RemovedInDjango40Warning
from django.utils.functional import cached_property
from django.utils.tree import Node
from django.contrib.auth.models import User
from django.db.models import QuerySet

def test_split_exclude():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user3 = User.objects.create(username='user3')

    # Assuming there's a method named 'exclude_users' for demonstration purposes
    # and we want to exclude users based on username.
    query = Query(User)

    # Use ~Q to define the exclusion condition
    filter_expr = ('username', 'user1')
    can_reuse = set()  # Define any reusable joins; empty for this example
    names_with_path = ('username',)  # Define the path for the filtering

    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    # Check condition structure
    assert isinstance(condition, BaseExpression)

    # Ensure that it contains an exclusion for user1
    assert 'NOT' in str(condition)
    assert 'user1' in str(condition)

    # Now check that excluding user1 results in user2 and user3
    results = list(query.exclude(username='user1'))
    assert len(results) == 2
    assert user2 in results
    assert user3 in results
    assert user1 not in results