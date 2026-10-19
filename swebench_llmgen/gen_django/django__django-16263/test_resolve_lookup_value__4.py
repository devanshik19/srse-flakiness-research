import pytest
from django.db.models.sql.query import Query
from django.db.models import F
from django.contrib.auth.models import User

def test_resolve_lookup_value_single_expression():
    query = Query(model=User, alias_cols=True)
    user_instance = User(username='testuser', email='test@example.com')
    
    resolved_value = query.resolve_lookup_value(F('username'), True, True)
    
    assert resolved_value is not None
    assert isinstance(resolved_value, F)
    assert resolved_value.name == 'username'

def test_resolve_lookup_value_list_of_expressions():
    query = Query(model=User, alias_cols=True)
    
    resolved_value = query.resolve_lookup_value([F('username'), F('email')], True, True)
    
    assert isinstance(resolved_value, list)
    assert len(resolved_value) == 2
    assert isinstance(resolved_value[0], F)
    assert isinstance(resolved_value[1], F)
    assert resolved_value[0].name == 'username'
    assert resolved_value[1].name == 'email'

def test_resolve_lookup_value_tuple_of_expressions():
    query = Query(model=User, alias_cols=True)
    
    resolved_value = query.resolve_lookup_value((F('username'), F('email')), True, True)
    
    assert isinstance(resolved_value, tuple)
    assert len(resolved_value) == 2
    assert isinstance(resolved_value[0], F)
    assert isinstance(resolved_value[1], F)
    assert resolved_value[0].name == 'username'
    assert resolved_value[1].name == 'email'

def test_resolve_lookup_value_namedtuple():
    from collections import namedtuple
    
    NamedValues = namedtuple('NamedValues', ['username', 'email'])
    query = Query(model=User, alias_cols=True)
    
    resolved_value = query.resolve_lookup_value(NamedValues(F('username'), F('email')), True, True)
    
    assert isinstance(resolved_value, NamedValues)
    assert isinstance(resolved_value.username, F)
    assert isinstance(resolved_value.email, F)
    assert resolved_value.username.name == 'username'
    assert resolved_value.email.name == 'email'

def test_resolve_lookup_value_non_expression():
    query = Query(model=User, alias_cols=True)

    resolved_value = query.resolve_lookup_value('test_value', True, True)
    
    assert resolved_value == 'test_value'