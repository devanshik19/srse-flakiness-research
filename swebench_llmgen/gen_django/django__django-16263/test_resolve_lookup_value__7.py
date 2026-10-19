import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def query():
    return Query(User)

def test_resolve_lookup_value_single_expression(query):
    class MockExpression:
        def resolve_expression(self, query, reuse, allow_joins):
            return "resolved_expression"
    
    result = query.resolve_lookup_value(MockExpression(), can_reuse=False, allow_joins=False)
    assert result == "resolved_expression"

def test_resolve_lookup_value_list_of_expressions(query):
    class MockExpression:
        def resolve_expression(self, query, reuse, allow_joins):
            return "resolved_expression"

    values = [MockExpression(), MockExpression()]
    result = query.resolve_lookup_value(values, can_reuse=False, allow_joins=False)
    assert result == ("resolved_expression", "resolved_expression")

def test_resolve_lookup_value_tuple_of_expressions(query):
    class MockExpression:
        def resolve_expression(self, query, reuse, allow_joins):
            return "resolved_expression"
    
    values = (MockExpression(), MockExpression())
    result = query.resolve_lookup_value(values, can_reuse=False, allow_joins=False)
    assert result == ("resolved_expression", "resolved_expression")

def test_resolve_lookup_value_namedtuple(query):
    from collections import namedtuple
    
    MockNamedTuple = namedtuple('MockNamedTuple', ['field1', 'field2'])
    
    class MockExpression:
        def resolve_expression(self, query, reuse, allow_joins):
            return "resolved_expression"

    values = MockNamedTuple(MockExpression(), MockExpression())
    result = query.resolve_lookup_value(values, can_reuse=False, allow_joins=False)
    assert result == MockNamedTuple("resolved_expression", "resolved_expression")