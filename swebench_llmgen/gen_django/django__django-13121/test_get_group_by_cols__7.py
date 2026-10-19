import copy
import datetime
from decimal import Decimal
from django.core.exceptions import EmptyResultSet, FieldError
from django.db import NotSupportedError, connection
from django.db.models import fields
from django.db.models.query_utils import Q
from django.utils.deconstruct import deconstructible
from django.utils.functional import cached_property
from django.utils.hashable import make_hashable
from django.contrib.auth.models import User
import pytest

class TestBaseExpression:
    @pytest.fixture
    def setup_user(self):
        user = User(username='testuser')
        user.set_password('testpassword')
        user.save()
        return user

    class TestExpression(BaseExpression):  # Create a test subclass to facilitate testing
        def __init__(self, output_field=None, contains_aggregate=False):
            self.output_field = output_field
            self._contains_aggregate = contains_aggregate
            self.source_expressions = []

        @property
        def contains_aggregate(self):
            return self._contains_aggregate

        def get_source_expressions(self):
            return self.source_expressions

        def add_source_expression(self, expression):
            self.source_expressions.append(expression)

    def test_get_group_by_cols_no_aggregate(self):
        expr = self.TestExpression(contains_aggregate=False)
        result = expr.get_group_by_cols()
        assert result == [expr]

    def test_get_group_by_cols_with_aggregate(self):
        expr1 = self.TestExpression(contains_aggregate=True)
        expr2 = self.TestExpression(contains_aggregate=False)
        expr1.add_source_expression(expr2)
        
        result = expr1.get_group_by_cols()
        assert result == [expr2]