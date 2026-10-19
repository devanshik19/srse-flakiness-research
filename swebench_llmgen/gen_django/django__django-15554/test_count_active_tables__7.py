import copy
import difflib
import functools
import sys
from collections import Counter, namedtuple
from collections.abc import Iterator, Mapping
from itertools import chain, count, product
from string import ascii_uppercase
from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db import DEFAULT_DB_ALIAS, NotSupportedError, connections
from django.db.models.aggregates import Count
from django.db.models.constants import LOOKUP_SEP
from django.db.models.expressions import (
    BaseExpression,
    Col,
    Exists,
    F,
    OuterRef,
    Ref,
    ResolvedOuterRef,
)
from django.db.models.fields import Field
from django.db.models.fields.related_lookups import MultiColSource
from django.db.models.lookups import Lookup
from django.db.models.query_utils import (
    Q,
    check_rel_lookup_compatibility,
    refs_expression,
)
from django.db.models.sql.constants import INNER, LOUTER, ORDER_DIR, SINGLE
from django.db.models.sql.datastructures import BaseTable, Empty, Join, MultiJoin
from django.db.models.sql.where import AND, OR, ExtraWhere, NothingNode, WhereNode
from django.utils.functional import cached_property
from django.utils.tree import Node
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_count_active_tables():
    # Create a Query instance using a user model
    user_query = Query(User, alias_cols={'id': 'id'})
    
    # Test with no active tables initially
    user_query.alias_refcount = {'user': 0}  # Simulate no active tables
    assert user_query.count_active_tables() == 0

    # Test with one active table
    user_query.alias_refcount = {'user': 1}  # Simulate one active table
    assert user_query.count_active_tables() == 1

    # Test with multiple active tables
    user_query.alias_refcount = {'user': 2, 'profile': 1}  # Simulate multiple active tables
    assert user_query.count_active_tables() == 2

    # Test with no active tables again
    user_query.alias_refcount = {'user': 0, 'profile': 0}  # No active tables
    assert user_query.count_active_tables() == 0