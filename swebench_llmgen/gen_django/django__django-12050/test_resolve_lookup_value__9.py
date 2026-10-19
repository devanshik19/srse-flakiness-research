import pytest
from django.db.models import F
from django.db.models.sql.query import Query
from django.contrib.auth.models import User

def test_resolve_lookup_value_single_expression():
    query = Query(User)
    expression = F('username')
    resolved_value = query.resolve_lookup_value(expression, True, True, False)
    assert resolved_value == expression.resolve_expression(query, reuse=True, allow_joins=True, simple_col=False)

def test_resolve_lookup_value_list_of_expressions():
    query = Query(User)
    expressions = [F('username'), F('email')]
    resolved_values = query.resolve_lookup_value(expressions, True, True, False)
    
    assert len(resolved_values) == 2
    assert resolved_values[0] == F('username').resolve_expression(query, reuse=True, allow_joins=True, simple_col=False)
    assert resolved_values[1] == F('email').resolve_expression(query, reuse=True, allow_joins=True, simple_col=False)

def test_resolve_lookup_value_mixed_values():
    query = Query(User)
    values = [F('username'), 'test@example.com', F('email')]
    resolved_values = query.resolve_lookup_value(values, True, True, False)
    
    assert len(resolved_values) == 3
    assert resolved_values[0] == F('username').resolve_expression(query, reuse=True, allow_joins=True, simple_col=False)
    assert resolved_values[1] == 'test@example.com'
    assert resolved_values[2] == F('email').resolve_expression(query, reuse=True, allow_joins=True, simple_col=False)

def test_resolve_lookup_value_no_expression():
    query = Query(User)
    non_expression_value = 'simple_value'
    resolved_value = query.resolve_lookup_value(non_expression_value, True, True, False)
    assert resolved_value == non_expression_value