import pytest
from django.db.models.query_utils import Q
from django.contrib.auth.models import User

def test_q_init_with_args():
    q = Q('name', 'John', _connector='AND', _negated=False)
    assert q.children == ['name', 'John']
    assert q.connector == 'AND'
    assert not q.negated

def test_q_init_with_kwargs():
    q = Q(name='John', age=30, _connector='OR', _negated=True)
    assert sorted(q.children) == [ ('age', 30), ('name', 'John') ]
    assert q.connector == 'OR'
    assert q.negated

def test_q_init_empty():
    q = Q()
    assert q.children == []
    assert q.connector is None
    assert not q.negated

def test_q_init_with_various_negations():
    q1 = Q('name', 'Alice', _negated=True)
    q2 = Q('name', 'Bob', _negated=False)
    assert q1.negated
    assert not q2.negated