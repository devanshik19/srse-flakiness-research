import pytest
from django.db.models import Query
from django.db.models.expressions import Value
from django.contrib.auth.models import User

class TestQueryResolveLookupValue:
    
    def setup_method(self):
        self.query = Query(model=User)

    def test_resolve_lookup_value_with_expression(self):
        expression = Value('example')  # An expression to resolve
        resolved_value = self.query.resolve_lookup_value(expression, can_reuse=True, allow_joins=True)
        assert resolved_value == expression

    def test_resolve_lookup_value_with_list(self):
        values = ['value1', Value('value2'), 'value3']
        resolved_values = self.query.resolve_lookup_value(values, can_reuse=True, allow_joins=True)
        assert resolved_values == ['value1', Value('value2'), 'value3']

    def test_resolve_lookup_value_with_tuple(self):
        values = ('value1', Value('value2'), 'value3')
        resolved_values = self.query.resolve_lookup_value(values, can_reuse=True, allow_joins=True)
        assert resolved_values == ('value1', Value('value2'), 'value3')

    def test_resolve_lookup_value_with_namedtuple(self):
        NamedTuple = namedtuple('NamedTuple', ['a', 'b'])
        values = NamedTuple('value1', Value('value2'))
        resolved_value = self.query.resolve_lookup_value(values, can_reuse=True, allow_joins=True)
        assert isinstance(resolved_value, NamedTuple)
        assert resolved_value.a == 'value1'
        assert resolved_value.b == Value('value2')

    def test_resolve_lookup_value_with_unsupported_type(self):
        value = 123  # An unsupported type
        resolved_value = self.query.resolve_lookup_value(value, can_reuse=True, allow_joins=True)
        assert resolved_value == 123