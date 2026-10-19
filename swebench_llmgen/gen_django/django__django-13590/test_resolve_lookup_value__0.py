import copy
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
from django.db.models.expressions import BaseExpression, Col, F, OuterRef, Ref
from django.db.models.fields import Field
from django.db.models.fields.related_lookups import MultiColSource
from django.db.models.lookups import Lookup
from django.db.models.query_utils import (
    Q, check_rel_lookup_compatibility, refs_expression,
)
from django.db.models.sql.constants import INNER, LOUTER, ORDER_DIR, SINGLE
from django.db.models.sql.datastructures import (
    BaseTable, Empty, Join, MultiJoin,
)
from django.db.models.sql.where import (
    AND, OR, ExtraWhere, NothingNode, WhereNode,
)
from django.utils.deprecation import RemovedInDjango40Warning
from django.utils.functional import cached_property
from django.utils.tree import Node
from django.db.models import QuerySet
from django.contrib.auth.models import User

class TestQuery:
    def test_resolve_lookup_value_with_expression(self):
        user = User(username='testuser', email='test@example.com')
        lookup_value = F('username')
        query = Query(model=User, where=None, alias_cols=False)
        
        resolved_value = query.resolve_lookup_value(lookup_value, can_reuse=True, allow_joins=False)
        assert resolved_value == lookup_value.resolve_expression(query, reuse=True, allow_joins=False)

    def test_resolve_lookup_value_with_iterable(self):
        user = User(username='testuser', email='test@example.com')
        query = Query(model=User, where=None, alias_cols=False)
        
        resolved_values = query.resolve_lookup_value(['testuser', 'test@example.com'], can_reuse=True, allow_joins=False)
        assert resolved_values == ['testuser', 'test@example.com']

    def test_resolve_lookup_value_with_empty_iterable(self):
        query = Query(model=User, where=None, alias_cols=False)
        
        resolved_values = query.resolve_lookup_value([], can_reuse=True, allow_joins=False)
        assert resolved_values == []

    def test_resolve_lookup_value_with_nested_iterable(self):
        query = Query(model=User, where=None, alias_cols=False)
        
        resolved_values = query.resolve_lookup_value([F('username'), ['test@example.com', 'testuser']], can_reuse=True, allow_joins=False)
        assert resolved_values[0] == F('username').resolve_expression(query, reuse=True, allow_joins=False)
        assert resolved_values[1] == ['test@example.com', 'testuser']