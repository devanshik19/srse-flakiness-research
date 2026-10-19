import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_resolve_lookup_value_single_expression():
    query = Query(model=User)
    expr = F('username')
    resolved = query.resolve_lookup_value(expr, can_reuse=False, allow_joins=False, simple_col=True)
    assert isinstance(resolved, F)
    assert resolved.name == 'username'

def test_resolve_lookup_value_list_of_expressions():
    query = Query(model=User)
    exprs = [F('username'), F('email')]
    resolved = query.resolve_lookup_value(exprs, can_reuse=False, allow_joins=False, simple_col=True)
    assert isinstance(resolved, tuple)
    assert len(resolved) == 2
    assert resolved[0].name == 'username'
    assert resolved[1].name == 'email'

def test_resolve_lookup_value_mixed_iterable():
    query = Query(model=User)
    exprs = [F('username'), 'test@example.com', F('first_name')]
    resolved = query.resolve_lookup_value(exprs, can_reuse=False, allow_joins=False, simple_col=True)
    assert isinstance(resolved, tuple)
    assert len(resolved) == 3
    assert resolved[0].name == 'username'
    assert resolved[1] == 'test@example.com'
    assert resolved[2].name == 'first_name'

def test_resolve_lookup_value_non_expressions():
    query = Query(model=User)
    value = 'simple_string'
    resolved = query.resolve_lookup_value(value, can_reuse=False, allow_joins=False, simple_col=True)
    assert resolved == 'simple_string'

def test_resolve_lookup_value_empty_list():
    query = Query(model=User)
    value = []
    resolved = query.resolve_lookup_value(value, can_reuse=False, allow_joins=False, simple_col=True)
    assert resolved == tuple()

def test_resolve_lookup_value_none():
    query = Query(model=User)
    resolved = query.resolve_lookup_value(None, can_reuse=False, allow_joins=False, simple_col=True)
    assert resolved is None