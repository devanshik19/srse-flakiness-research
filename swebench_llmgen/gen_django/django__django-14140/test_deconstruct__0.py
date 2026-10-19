import pytest
from django.contrib.auth.models import User
from django.db.models import Q

def test_deconstruct_single_child():
    q = Q(('username', 'testuser'))
    path, args, kwargs = q.deconstruct()
    assert path == 'django.db.models.Q'
    assert args == ()
    assert kwargs == {'username': 'testuser'}

def test_deconstruct_multiple_children():
    q = Q(('username', 'testuser'), ('email', 'test@example.com'))
    path, args, kwargs = q.deconstruct()
    assert path == 'django.db.models.Q'
    assert args == (('username', 'testuser'), ('email', 'test@example.com'))
    assert '_connector' not in kwargs

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