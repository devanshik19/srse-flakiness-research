import pytest
from django.db.models.query_utils import Q
from django.contrib.auth.models import User

def test_deconstruct_single_child():
    q_obj = Q(('username', 'testuser'))
    path, args, kwargs = q_obj.deconstruct()
    
    assert path == 'django.db.models.Q'
    assert args == ()
    assert kwargs == {'username': 'testuser'}

def test_deconstruct_multiple_children():
    q_obj = Q('username', 'testuser', connector=Q.AND, negated=False)
    path, args, kwargs = q_obj.deconstruct()
    
    assert path == 'django.db.models.Q'
    assert args == (('username', 'testuser'),)
    assert kwargs == {}

def test_deconstruct_negated():
    q_obj = Q(('username', 'testuser'), negated=True)
    path, args, kwargs = q_obj.deconstruct()
    
    assert path == 'django.db.models.Q'
    assert args == (('username', 'testuser'),)
    assert kwargs == {'_negated': True}

def test_deconstruct_path_replacement():
    q_obj = Q('username', 'testuser', connector=Q.OR)
    path, args, kwargs = q_obj.deconstruct()
    
    assert path == 'django.db.models.Q'
    assert args == (('username', 'testuser'),)
    assert kwargs == {'_connector': Q.OR}