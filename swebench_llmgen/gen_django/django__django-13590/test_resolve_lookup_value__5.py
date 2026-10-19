import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_resolve_lookup_value_expr():
    query = Query(model=User, where=None, alias_cols=None)
    user_instance = User(username='testuser')
    resolved_value = query.resolve_lookup_value(user_instance, can_reuse=False, allow_joins=True)
    assert resolved_value == user_instance

def test_resolve_lookup_value_list():
    query = Query(model=User, where=None, alias_cols=None)
    user1 = User(username='testuser1')
    user2 = User(username='testuser2')
    resolved_values = query.resolve_lookup_value([user1, user2], can_reuse=False, allow_joins=True)
    assert resolved_values == [user1, user2]

def test_resolve_lookup_value_tuple():
    query = Query(model=User, where=None, alias_cols=None)
    user1 = User(username='testuser1')
    user2 = User(username='testuser2')
    resolved_values = query.resolve_lookup_value((user1, user2), can_reuse=False, allow_joins=True)
    assert resolved_values == (user1, user2)

def test_resolve_lookup_value_non_expression():
    query = Query(model=User, where=None, alias_cols=None)
    resolved_value = query.resolve_lookup_value(123, can_reuse=False, allow_joins=True)
    assert resolved_value == 123

def test_resolve_lookup_value_empty():
    query = Query(model=User, where=None, alias_cols=None)
    resolved_value = query.resolve_lookup_value(None, can_reuse=False, allow_joins=True)
    assert resolved_value is None