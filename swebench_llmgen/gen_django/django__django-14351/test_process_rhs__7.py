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
        return not callable(self.rhs)

    def get_db_prep_lookup(self, value, connection):
        if isinstance(value, str):
            return [value], []
        return [value]

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

class DummyCompiler:
    def compile(self, value):
        if isinstance(value, Value):
            return str(value.value), []
        return str(value)

@pytest.mark.django_db
def test_process_rhs():
    # Setup
    user = User.objects.create(username='testuser')
    lhs = CharField()  # Assuming lhs is a CharField
    lookup = Lookup(lhs, user.username)

    # Test direct value case
    compiler = DummyCompiler()
    connection = None  # Simulating a database connection
    sql, params = lookup.process_rhs(compiler, connection)
    assert sql == '(testuser)'  # Expecting the SQL to wrap the testuser in parentheses
    assert params == []  # No parameters since it's plain value

    # Test with bilateral transforms
    lookup.bilateral_transforms.append(lambda value: value.upper())
    sql, params = lookup.process_rhs(compiler, connection)
    assert sql == '(TESTUSER)'
    assert params == []

    # Test callable rhs
    lookup.rhs = Value('new_value', output_field=lhs)
    sql, params = lookup.process_rhs(compiler, connection)
    assert sql == "(new_value)"
    assert params == []

    # Test with as_sql method
    lookup.rhs = Case(When(pk=1, then=Value('True')), default=Value('False'))
    sql, params = lookup.process_rhs(compiler, connection)
    assert sql == "(CASE WHEN (pk = 1) THEN True ELSE False END)"
    assert params == []