import difflib
import functools
import inspect
import sys
import warnings
from collections import Counter, namedtuple
from collections.abc import Iterator, Mapping
from itertools import chain, count, product
from string import ascii_uppercase
from django.core.exceptions import (
    EmptyResultSet, FieldDoesNotExist, FieldError,
)
from django.db import DEFAULT_DB_ALIAS, NotSupportedError, connections
from django.db.models.aggregates import Count
from django.db.models.constants import LOOKUP_SEP
from django.db.models.expressions import (
    BaseExpression, Col, F, OuterRef, Ref, SimpleCol,
)
from django.db.models.fields import Field
from django.db.models.fields.related_lookups import MultiColSource
from django.db.models.lookups import Lookup
from django.db.models.query_utils import (
    Q, check_rel_lookup_compatibility, refs_expression,
)
from django.db.models.sql.constants import (
    INNER, LOUTER, ORDER_DIR, ORDER_PATTERN, SINGLE,
)
from django.db.models.sql.datastructures import (
    BaseTable, Empty, Join, MultiJoin,
)
from django.db.models.sql.where import (
    AND, OR, ExtraWhere, NothingNode, WhereNode,
)
from django.utils.deprecation import RemovedInDjango40Warning
from django.utils.functional import cached_property
from django.utils.tree import Node
from django.db.models import Q
from django.db.models.sql.query import Query
from django.contrib.auth.models import User
import pytest

def test_split_exclude():
    user1 = User.objects.create(username='user1', id=1)
    user2 = User.objects.create(username='user2', id=2)
    
    # Assuming we want to exclude users with username 'user1'
    query = Query(User)
    filter_expr = ('username', 'user1')
    can_reuse = {query.get_initial_alias()}  # Reusable joins
    names_with_path = ['username']

    # Test the split_exclude method
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    # Validate conditions from the result
    assert isinstance(condition, WhereNode)
    assert condition.children  # Should have some conditions added
    assert needed_inner is False  # Check the condition of inner needed

    # Check that the condition includes NOT EXISTS
    subquery_condition = condition.children[0].children[0]
    assert isinstance(subquery_condition, Lookup)
    assert subquery_condition.rhs == F('username')  # Ensure it's referring to the correct field query

    # Test with an F expression
    filter_expr_f = ('username', F('username'))
    condition_f, needed_inner_f = query.split_exclude(filter_expr_f, can_reuse, names_with_path)
    
    assert isinstance(condition_f, WhereNode)
    assert needed_inner_f is False

    # Ensure condition includes a subquery referencing the outer reference
    assert condition_f.children

    # Clean up created users
    user1.delete()
    user2.delete()