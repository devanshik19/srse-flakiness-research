import pytest
from django.db.models.query_utils import Q
from django.contrib.auth.models import User

def test_q_init_with_args():
    q = Q(User.username='test_user', User.email='test@example.com')
    assert len(q.children) == 2
    assert q.children[0] == ('username', 'test_user')
    assert q.children[1] == ('email', 'test@example.com')

def test_q_init_with_kwargs():
    q = Q(_connector='AND', _negated=True, username='test_user', email='test@example.com')
    assert len(q.children) == 2
    assert q.children[0] == ('email', 'test@example.com')
    assert q.children[1] == ('username', 'test_user')
    assert q.connector == 'AND'
    assert q.negated is True

def test_q_init_empty():
    q = Q()
    assert len(q.children) == 0

def test_q_init_with_negation():
    q = Q(_negated=True)
    assert q.negated is True
    assert len(q.children) == 0