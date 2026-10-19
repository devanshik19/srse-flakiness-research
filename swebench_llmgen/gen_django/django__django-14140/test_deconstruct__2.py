import pytest
from django.contrib.auth.models import User
from django.db.models import Q

def test_deconstruct_single_child():
    q = Q(('username', 'test_user'))

    path, args, kwargs = q.deconstruct()
    
    assert path == 'django.db.models.Q'
    assert args == ()
    assert kwargs == {'username': 'test_user'}

def test_deconstruct_multiple_children():
    q = Q(('username', 'test_user'), ('email', 'test@example.com'))

    path, args, kwargs = q.deconstruct()
    
    assert path == 'django.db.models.Q'
    assert args == (('username', 'test_user'), ('email', 'test@example.com'))
    assert kwargs == {}

def test_deconstruct_with_connector():
    q = Q(('username', 'test_user'), ('email', 'test@example.com'), connector=Q.AND)

    path, args, kwargs = q.deconstruct()

    assert path == 'django.db.models.Q'
    assert args == (('username', 'test_user'), ('email', 'test@example.com'))
    assert kwargs == {'_connector': Q.AND}

def test_deconstruct_negated():
    q = ~Q(('username', 'test_user'))

    path, args, kwargs = q.deconstruct()

    assert path == 'django.db.models.Q'
    assert args == (('username', 'test_user'),)
    assert kwargs == {'_negated': True}