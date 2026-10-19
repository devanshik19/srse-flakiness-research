import pytest
from django.contrib.auth.models import User
from django.db.models.query_utils import Q

def test_deconstruct_single_child():
    q_obj = Q((('username', 'testuser'),))
    q_obj.children = [(('username', 'testuser'),)]
    q_obj.connector = q_obj.default
    q_obj.negated = False

    path, args, kwargs = q_obj.deconstruct()
    
    assert path == 'django.db.models.query_utils.Q'
    assert args == (('username', 'testuser'),)
    assert kwargs == {}

def test_deconstruct_multiple_children():
    q_obj = Q((('username', 'testuser'), ('email', 'test@example.com')))
    q_obj.children = [(('username', 'testuser'),), (('email', 'test@example.com'),)]
    q_obj.connector = q_obj.default
    q_obj.negated = False

    path, args, kwargs = q_obj.deconstruct()
    
    assert path == 'django.db.models.query_utils.Q'
    assert args == (('username', 'testuser'), ('email', 'test@example.com'))
    assert kwargs == {}

def test_deconstruct_with_negation():
    q_obj = Q(('username', 'testuser'))
    q_obj.children = [(('username', 'testuser'),)]
    q_obj.connector = q_obj.default
    q_obj.negated = True

    path, args, kwargs = q_obj.deconstruct()

    assert path == 'django.db.models.query_utils.Q'
    assert args == (('username', 'testuser'),)
    assert kwargs == {'_negated': True}

def test_deconstruct_with_default_path():
    q_obj = Q(('username', 'testuser'))
    q_obj.children = [('username', 'testuser')]
    q_obj.connector = q_obj.default
    q_obj.negated = False

    path, args, kwargs = q_obj.deconstruct()

    assert path == 'django.db.models.Q'
    assert args == (('username', 'testuser'),)
    assert kwargs == {}