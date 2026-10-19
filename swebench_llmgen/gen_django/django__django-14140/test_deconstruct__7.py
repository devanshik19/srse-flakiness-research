import pytest
from django.db.models.query_utils import Q
from django.contrib.auth.models import User

def test_deconstruct_single_child():
    q = Q(('username', 'testuser'))
    path, args, kwargs = q.deconstruct()
    
    assert path == 'django.db.models.query_utils.Q'
    assert args == ()
    assert kwargs == {'username': 'testuser'}

def test_deconstruct_multiple_children():
    q = Q(('username', 'testuser'), ('email', 'test@example.com'), connector=Q.AND)
    path, args, kwargs = q.deconstruct()
    
    assert path == 'django.db.models.query_utils.Q'
    assert args == (('username', 'testuser'), ('email', 'test@example.com'))
    assert kwargs == {'_connector': Q.AND}

def test_deconstruct_negation():
    q = ~Q(('username', 'testuser'))
    path, args, kwargs = q.deconstruct()
    
    assert path == 'django.db.models.query_utils.Q'
    assert args == (('username', 'testuser'),)
    assert kwargs == {'_negated': True}

def test_deconstruct_with_default_connector():
    q = Q(('username', 'testuser'), Q(('email', 'test@example.com')))
    path, args, kwargs = q.deconstruct()

    assert path == 'django.db.models.query_utils.Q'
    assert args == (('username', 'testuser'), ('email', 'test@example.com'))
    assert kwargs == {}