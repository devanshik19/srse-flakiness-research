import itertools
import math
from copy import copy
from django.core.exceptions import EmptyResultSet
from django.db.models.expressions import Case, Func, Value, When
from django.db.models.fields import (
    CharField, DateTimeField, Field, IntegerField, UUIDField,
)
from django.db.models.query_utils import RegisterLookupMixin
from django.utils.datastructures import OrderedSet
from django.utils.functional import cached_property
from django.utils.hashable import make_hashable
from django.contrib.auth.models import User
from django.db.models import Q

class Lookup:
    # Focal class as provided
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.lookup_name = 'exact'  # For example purposes
        self.bilateral_transforms = False  # Default value

    def rhs_is_direct_value(self):
        return isinstance(self.rhs, (int, str))  # Simplification for the test

    def apply_bilateral_transforms(self, value):
        return copy(value)

    def get_db_prep_lookup(self, value, connection):
        return [value], []

    def process_rhs(self, compiler, connection):
        value = self.rhs
        if self.bilateral_transforms:
            if self.rhs_is_direct_value():
                value = Value(value, output_field=self.lhs.output_field)
            value = self.apply_bilateral_transforms(value)
            value = value.resolve_expression(compiler.query)
        if hasattr(value, 'as_sql'):
            sql, params = compiler.compile(value)
            if sql and sql[0] != '(':
                sql = '(%s)' % sql
            return sql, params
        else:
            return self.get_db_prep_lookup(value, connection)

def test_process_rhs():
    # Set up a dummy lhs and compiler since we don't have full Django context here.
    class DummyField(Field):
        output_field = CharField()  # Simplified for the test

    class DummyCompiler:
        def compile(self, value):
            return str(value), []

    lhs = DummyField()
    compiler = DummyCompiler()
    connection = None  # Use a mock or any placeholder that fits your logic

    # Case where rhs is a direct value
    lookup = Lookup(lhs, 'test_value')
    sql, params = lookup.process_rhs(compiler, connection)
    assert sql == "'test_value'"
    assert params == []

    # Case where rhs is an integer
    lookup = Lookup(lhs, 123)
    sql, params = lookup.process_rhs(compiler, connection)
    assert sql == '[123]'
    assert params == []

    # Case where bilateral transforms are enabled
    lookup.bilateral_transforms = True
    lookup = Lookup(lhs, 'test_value')
    sql, params = lookup.process_rhs(compiler, connection)
    assert sql == "'test_value'"
    assert params == []

    # Verify that if value has as_sql, it process correctly
    class SqlExpr:
        def as_sql(self):
            return 'sql_expression', []

    lookup = Lookup(lhs, SqlExpr())
    sql, params = lookup.process_rhs(compiler, connection)
    assert sql == '(sql_expression)'
    assert params == []

    # Edge case where EmptyResultSet might be raised
    with pytest.raises(EmptyResultSet):
        # To simulate a situation that might raise an EmptyResultSet
        pass  # This would normally be some logic that triggers the exception