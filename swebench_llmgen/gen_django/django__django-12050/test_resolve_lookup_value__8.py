import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_resolve_lookup_value_single_expression():
    query = Query(model=User)
    expression = F('username')
    resolved_value = query.resolve_lookup_value(expression, can_reuse=True, allow_joins=False, simple_col=False)
    assert resolved_value == expression.resolve_expression(query, reuse=True, allow_joins=False, simple_col=False)

def test_resolve_lookup_value_list_expressions():
    query = Query(model=User)
    expression_list = [F('username'), 'test@example.com']
    resolved_value = query.resolve_lookup_value(expression_list, can_reuse=True, allow_joins=False, simple_col=False)
    assert len(resolved_value) == 2
    assert resolved_value[0] == F('username').resolve_expression(query, reuse=True, allow_joins=False, simple_col=False)
    assert resolved_value[1] == 'test@example.com'

def test_resolve_lookup_value_tuple_expressions():
    query = Query(model=User)
    expression_tuple = (F('email'), F('is_active'))
    resolved_value = query.resolve_lookup_value(expression_tuple, can_reuse=True, allow_joins=False, simple_col=False)
    assert isinstance(resolved_value, tuple)
    assert len(resolved_value) == 2
    assert resolved_value[0] == F('email').resolve_expression(query, reuse=True, allow_joins=False, simple_col=False)
    assert resolved_value[1] == F('is_active').resolve_expression(query, reuse=True, allow_joins=False, simple_col=False)

def test_resolve_lookup_value_no_expression():
    query = Query(model=User)
    resolved_value = query.resolve_lookup_value('plain_value', can_reuse=True, allow_joins=False, simple_col=False)
    assert resolved_value == 'plain_value'