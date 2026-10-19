import pytest
from django.db.models import Query
from django.contrib.auth.models import User

def test_resolve_lookup_value_expression():
    query = Query(User)
    expression = User.username  # Example expression (should be resolved)
    
    resolved_value = query.resolve_lookup_value(expression, can_reuse=True, allow_joins=True)
    assert resolved_value == expression

def test_resolve_lookup_value_list():
    query = Query(User)
    expressions = [User.username, User.email]
    
    resolved_value = query.resolve_lookup_value(expressions, can_reuse=True, allow_joins=True)
    assert isinstance(resolved_value, list)
    assert len(resolved_value) == 2
    assert all(isinstance(val, str) for val in resolved_value)

def test_resolve_lookup_value_namedtuple():
    UserTuple = namedtuple('UserTuple', ['username', 'email'])
    query = Query(User)
    expressions = UserTuple(User.username, User.email)
    
    resolved_value = query.resolve_lookup_value(expressions, can_reuse=True, allow_joins=True)
    assert isinstance(resolved_value, UserTuple)
    assert resolved_value.username == expressions.username
    assert resolved_value.email == expressions.email

def test_resolve_lookup_value_empty():
    query = Query(User)
    
    resolved_value = query.resolve_lookup_value(None, can_reuse=True, allow_joins=True)
    assert resolved_value is None