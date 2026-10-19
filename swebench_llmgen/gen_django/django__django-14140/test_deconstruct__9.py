import pytest
from django.db.models.query_utils import Q
from django.contrib.auth.models import User

def test_deconstruct_single_child():
    q = Q(('username', 'testuser'))
    path, args, kwargs = q.deconstruct()
    assert path == 'django.db.models.Q'
    assert args == ()
    assert kwargs == {'username': 'testuser'}

def test_deconstruct_multiple_children():
    q = Q(('username', 'testuser'), ('is_active', True))
    path, args, kwargs = q.deconstruct()
    assert path == 'django.db.models.Q'
    assert args == (('username', 'testuser'), ('is_active', True))
    assert kwargs == {}

def test_deconstruct_with_connector():
    q = Q(('username', 'testuser'), connector=Q.AND)
    path, args, kwargs = q.deconstruct()
    assert path == 'django.db.models.Q'
    assert args == (('username', 'testuser'),)
    assert kwargs == {'_connector': Q.AND}

def test_deconstruct_negated():
    q = ~Q(('username', 'testuser'))
    path, args, kwargs = q.deconstruct()
    assert path == 'django.db.models.Q'
    assert args == (('username', 'testuser'),)
    assert kwargs == {'_negated': True}

def test_deconstruct_empty():
    q = Q()
    path, args, kwargs = q.deconstruct()
    assert path == 'django.db.models.Q'
    assert args == ()
    assert kwargs == {}