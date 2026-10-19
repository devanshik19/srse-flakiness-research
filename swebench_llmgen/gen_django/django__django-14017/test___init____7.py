import pytest
from django.contrib.auth.models import User
from django.db.models.query_utils import Q

def test_q_init_with_args():
    q_instance = Q(User=username='testuser')
    assert isinstance(q_instance, Q)
    assert q_instance.children == [('username', 'testuser')]
    assert q_instance.connector is None
    assert not q_instance.negated

def test_q_init_with_kwargs():
    q_instance = Q(username='testuser', email='test@example.com')
    assert isinstance(q_instance, Q)
    assert sorted(q_instance.children) == [('email', 'test@example.com'), ('username', 'testuser')]
    assert q_instance.connector is None
    assert not q_instance.negated

def test_q_init_with_connector():
    q_instance = Q(User=username='testuser', _connector='OR')
    assert isinstance(q_instance, Q)
    assert q_instance.children == [('username', 'testuser')]
    assert q_instance.connector == 'OR'
    assert not q_instance.negated

def test_q_init_with_negated():
    q_instance = Q(User=username='testuser', _negated=True)
    assert isinstance(q_instance, Q)
    assert q_instance.children == [('username', 'testuser')]
    assert q_instance.connector is None
    assert q_instance.negated

def test_q_init_with_both_connector_and_negated():
    q_instance = Q(User=username='testuser', _connector='AND', _negated=True)
    assert isinstance(q_instance, Q)
    assert q_instance.children == [('username', 'testuser')]
    assert q_instance.connector == 'AND'
    assert q_instance.negated