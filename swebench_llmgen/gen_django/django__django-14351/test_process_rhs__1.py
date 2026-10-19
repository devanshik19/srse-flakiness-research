import itertools
import math
from copy import copy
from django.core.exceptions import EmptyResultSet
from django.db.models.expressions import Case, Func, Value, When
from django.db.models.fields import CharField, DateTimeField, Field, IntegerField, UUIDField
from django.db.models.query_utils import RegisterLookupMixin
from django.utils.datastructures import OrderedSet
from django.utils.functional import cached_property
from django.utils.hashable import make_hashable
from django.contrib.auth.models import User
import pytest

class TestLookup:
    
    @pytest.fixture
    def setup_lookup(self):
        class MockLookup:
            def __init__(self, lhs, rhs):
                self.lhs = lhs
                self.rhs = rhs
                self.bilateral_transforms = False

            def rhs_is_direct_value(self):
                return isinstance(self.rhs, (int, str))

            def apply_bilateral_transforms(self, value):
                return Value(value)

            def get_db_prep_lookup(self, value, connection):
                return ('SELECT * FROM example WHERE field = %s', [value])

        return MockLookup

    def test_process_rhs_direct_value(self, setup_lookup):
        lookup = setup_lookup('lhs', 'test_value')
        compiler = None  # Mocked compiler; replace if needed
        connection = None  # Mocked connection; replace if needed

        sql, params = lookup.process_rhs(compiler, connection)

        assert sql == 'SELECT * FROM example WHERE field = %s'
        assert params == ['test_value']

    def test_process_rhs_bilateral_transforms(self, setup_lookup):
        def mock_apply_bilateral_transforms(self, value):
            return Value(value + '_transformed')

        lookup = setup_lookup('lhs', 'test_value')
        lookup.bilateral_transforms = True
        lookup.apply_bilateral_transforms = mock_apply_bilateral_transforms.__get__(lookup)

        compiler = None  # Mocked compiler; replace if needed
        connection = None  # Mocked connection; replace if needed

        sql, params = lookup.process_rhs(compiler, connection)

        assert sql == 'SELECT * FROM example WHERE field = %s'
        assert params == ['test_value_transformed']

    def test_process_rhs_expression(self, setup_lookup):
        class MockExpression:
            def as_sql(self, compiler, connection):
                return ('SELECT * FROM example WHERE field = %s', ['mock_expression'])

        lookup = setup_lookup('lhs', MockExpression())
        compiler = None  # Mocked compiler; replace if needed
        connection = None  # Mocked connection; replace if needed

        sql, params = lookup.process_rhs(compiler, connection)

        assert sql == 'SELECT * FROM example WHERE field = %s'
        assert params == ['mock_expression']