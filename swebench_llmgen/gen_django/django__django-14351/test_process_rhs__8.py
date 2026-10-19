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

class Lookup:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.bilateral_transforms = []
        
    def apply_bilateral_transforms(self, value):
        for transform in self.bilateral_transforms:
            value = transform(value)
        return value
    
    def rhs_is_direct_value(self):
        return not hasattr(self.rhs, 'as_sql')

    def get_db_prep_lookup(self, value, connection):
        return value, []

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

class MockCompiler:
    def compile(self, value):
        return str(value), []

class MockConnection:
    pass

@pytest.mark.parametrize("rhs, bilateral_transforms, expected_sql", [
    ("test_value", [], "('test_value')", []),
    (Value("test_value", output_field=CharField()), 
     [], "('test_value')", []),
])
def test_process_rhs(rhs, bilateral_transforms, expected_sql):
    lhs = Value("dummy_lhs", output_field=CharField())
    lookup = Lookup(lhs, rhs)
    lookup.bilateral_transforms = bilateral_transforms
    compiler = MockCompiler()
    connection = MockConnection()
    
    sql, params = lookup.process_rhs(compiler, connection)
    
    assert sql == expected_sql[0]
    assert params == expected_sql[1]