import pytest
from django.contrib.auth.models import User
from django.db.models import Query

def test_resolve_lookup_value_expression():
    query = Query(model=User, where=None, alias_cols=None)
    
    class MockExpression:
        def resolve_expression(self, query, reuse, allow_joins):
            return 'resolved_expression'

    resolved_value = query.resolve_lookup_value(MockExpression(), can_reuse=True, allow_joins=True)
    assert resolved_value == 'resolved_expression'

def test_resolve_lookup_value_list():
    query = Query(model=User, where=None, alias_cols=None)
    
    class MockExpression:
        def resolve_expression(self, query, reuse, allow_joins):
            return 'resolved_expression'

    values = [MockExpression(), MockExpression()]
    resolved_values = query.resolve_lookup_value(values, can_reuse=True, allow_joins=True)
    assert resolved_values == ['resolved_expression', 'resolved_expression']

def test_resolve_lookup_value_tuple():
    query = Query(model=User, where=None, alias_cols=None)

    class MockExpression:
        def resolve_expression(self, query, reuse, allow_joins):
            return 'resolved_expression'

    values = (MockExpression(), MockExpression())
    resolved_values = query.resolve_lookup_value(values, can_reuse=True, allow_joins=True)
    assert resolved_values == ('resolved_expression', 'resolved_expression')

def test_resolve_lookup_value_direct_value():
    query = Query(model=User, where=None, alias_cols=None)
    value = 'direct_value'
    
    resolved_value = query.resolve_lookup_value(value, can_reuse=True, allow_joins=True)
    assert resolved_value == 'direct_value'