import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    return Query(User)

def test_resolve_lookup_value_single_expression(user_query):
    class DummyExpression:
        def resolve_expression(self, query, reuse, allow_joins):
            return "resolved_value"
    
    resolved_value = user_query.resolve_lookup_value(DummyExpression(), can_reuse=False, allow_joins=False)
    assert resolved_value == "resolved_value"

def test_resolve_lookup_value_list_of_expressions(user_query):
    class DummyExpression:
        def resolve_expression(self, query, reuse, allow_joins):
            return "resolved_value"
    
    values = [DummyExpression(), DummyExpression()]
    resolved_values = user_query.resolve_lookup_value(values, can_reuse=False, allow_joins=False)
    assert resolved_values == ("resolved_value", "resolved_value")

def test_resolve_lookup_value_tuple_of_expressions(user_query):
    class DummyExpression:
        def resolve_expression(self, query, reuse, allow_joins):
            return "resolved_value"
    
    values = (DummyExpression(), DummyExpression())
    resolved_values = user_query.resolve_lookup_value(values, can_reuse=False, allow_joins=False)
    assert resolved_values == ("resolved_value", "resolved_value")

def test_resolve_lookup_value_namedtuple(user_query):
    from collections import namedtuple
    DummyTuple = namedtuple('DummyTuple', 'field1 field2')
    
    class DummyExpression:
        def resolve_expression(self, query, reuse, allow_joins):
            return "resolved_value"
    
    values = DummyTuple(DummyExpression(), DummyExpression())
    resolved_values = user_query.resolve_lookup_value(values, can_reuse=False, allow_joins=False)
    assert resolved_values == DummyTuple("resolved_value", "resolved_value")

def test_resolve_lookup_value_non_expression(user_query):
    value = 42
    resolved_value = user_query.resolve_lookup_value(value, can_reuse=False, allow_joins=False)
    assert resolved_value == 42