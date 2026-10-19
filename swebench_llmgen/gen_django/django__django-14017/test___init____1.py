import pytest
from django.db.models.query_utils import Q
from django.contrib.auth.models import User
from django.core.exceptions import FieldError

def test_q_init_with_args():
    q1 = Q(User.objects.filter(username='user1'))
    assert isinstance(q1, Q)
    assert len(q1.children) == 1

def test_q_init_with_kwargs():
    q2 = Q(username='user2', _connector=Q.AND)
    assert isinstance(q2, Q)
    assert len(q2.children) == 1
    assert q2.children[0] == ('username', 'user2')

def test_q_init_with_negation():
    q3 = Q(User.objects.filter(username='user3'), _negated=True)
    assert isinstance(q3, Q)
    assert q3.negated is True
    assert len(q3.children) == 1

def test_q_init_with_both_args_and_kwargs():
    q4 = Q(User.objects.filter(username='user4'), age=30, _connector=Q.OR, _negated=True)
    assert isinstance(q4, Q)
    assert len(q4.children) == 2
    assert q4.negated is True

def test_q_init_with_empty():
    q5 = Q()
    assert isinstance(q5, Q)
    assert len(q5.children) == 0

def test_q_init_invalid_kwarg():
    with pytest.raises(FieldError):
        Q(invalid_field='value')