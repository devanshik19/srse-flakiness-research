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

from django.db.models import QuerySet
from django.contrib.auth.models import User

def test_count_active_tables():
    # Create an instance of Query with a dummy queryset
    queryset = User.objects.all()
    query = queryset.query

    # Manually modify the alias_refcount to simulate active tables
    query.alias_refcount[query.get_initial_alias()] = 1  # Set initial alias active
    query.alias_refcount[query.get_initial_alias() + '1'] = 2  # Another aliased table

    # Check active tables count
    count = query.count_active_tables()
    
    assert count == 2  # Expecting 2 active tables

    # Reset reference counts to simulate no active tables
    query.alias_refcount[query.get_initial_alias()] = 0
    query.alias_refcount[query.get_initial_alias() + '1'] = 0

    # Check active tables count again
    count = query.count_active_tables()

    assert count == 0  # Expecting 0 active tables