import copy
import datetime
from decimal import Decimal
from django.core.exceptions import EmptyResultSet, FieldError
from django.db import NotSupportedError, connection
from django.db.models import Expression
from django.db.models.constants import LOOKUP_SEP
from django.db.models.query_utils import Q
from django.utils.deconstruct import deconstructible
from django.utils.functional import cached_property
from django.utils.hashable import make_hashable
from django.contrib.auth.models import User
import pytest

class MockExpression(Expression):
    def __init__(self, contains_aggregate=False):
        self._contains_aggregate = contains_aggregate

    @property
    def contains_aggregate(self):
        return self._contains_aggregate

    def get_source_expressions(self):
        return [self] if not self._contains_aggregate else []

def test_get_group_by_cols_no_aggregate():
    expr = MockExpression(contains_aggregate=False)
    result = expr.get_group_by_cols()
    assert result == [expr]

def test_get_group_by_cols_with_aggregate():
    child_expr = MockExpression(contains_aggregate=False)
    parent_expr = MockExpression(contains_aggregate=True)
    parent_expr.get_source_expressions = lambda: [child_expr]

    result = parent_expr.get_group_by_cols()
    assert result == [child_expr]