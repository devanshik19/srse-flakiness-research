import pytest
from django.db.models.query_utils import Q
from django.contrib.auth.models import User

def test_q_init_with_positional_args():
    q = Q(User.objects.filter(username='testuser1'))
    assert isinstance(q, Q)
    assert len(q.children) == 1
    assert q.children[0].query.name == 'testuser1'

def test_q_init_with_keyword_args():
    q = Q(username='testuser2')
    assert isinstance(q, Q)
    assert len(q.children) == 1
    assert q.children[0] == ('username', 'testuser2')

def test_q_init_with_connector_and_negated():
    q = Q(User.objects.filter(username='testuser3'), _connector='OR', _negated=True)
    assert isinstance(q, Q)
    assert len(q.children) == 1
    assert q.children[0].query.name == 'testuser3'
    assert q.connector == 'OR'
    assert q.negated is True

def test_q_init_with_no_args():
    q = Q()
    assert isinstance(q, Q)
    assert len(q.children) == 0

def test_q_init_with_mixed_args():
    q = Q(User.objects.filter(username='testuser4'), password='password4')
    assert isinstance(q, Q)
    assert len(q.children) == 2
    assert q.children[0].query.name == 'testuser4'
    assert q.children[1] == ('password', 'password4')