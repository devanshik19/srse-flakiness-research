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
    # Create an instance of Query with an active alias_refcount
    query = Query(User)

    # Simulate the reference counts
    query.alias_refcount = {
        'user': 1,
        'profile': 0,
        'settings': 2,
    }

    # Count active tables
    active_table_count = query.count_active_tables()

    assert active_table_count == 2

    # Test with no active tables
    query.alias_refcount = {
        'user': 0,
        'profile': 0,
        'settings': 0,
    }

    active_table_count = query.count_active_tables()

    assert active_table_count == 0