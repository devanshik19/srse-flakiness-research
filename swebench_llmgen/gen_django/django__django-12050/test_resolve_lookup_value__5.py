import pytest
from django.db.models import F
from django.db.models.sql.query import Query
from django.contrib.auth.models import User

def test_resolve_lookup_value_single_expression():
    q = Query(model=User)
    expression = F('username')
    result = q.resolve_lookup_value(expression, can_reuse=True, allow_joins=True, simple_col=True)
    assert result == expression.resolve_expression(q, reuse=True, allow_joins=True, simple_col=True)

def test_resolve_lookup_value_list_of_expressions():
    q = Query(model=User)
    expressions = [F('username'), F('email')]
    result = q.resolve_lookup_value(expressions, can_reuse=True, allow_joins=True, simple_col=True)
    expected_result = (
        F('username').resolve_expression(q, reuse=True, allow_joins=True, simple_col=True),
        F('email').resolve_expression(q, reuse=True, allow_joins=True, simple_col=True),
    )
    assert result == expected_result

def test_resolve_lookup_value_mixed_types():
    q = Query(model=User)
    values = [F('username'), 'test@example.com', 123]
    result = q.resolve_lookup_value(values, can_reuse=True, allow_joins=True, simple_col=False)
    expected_result = (
        F('username').resolve_expression(q, reuse=True, allow_joins=True, simple_col=False),
        'test@example.com',
        123,
    )
    assert result == expected_result

def test_resolve_lookup_value_no_expression():
    q = Query(model=User)
    value = 'simple_value'
    result = q.resolve_lookup_value(value, can_reuse=False, allow_joins=False, simple_col=False)
    assert result == 'simple_value'