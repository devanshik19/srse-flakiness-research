import pytest
from django.db.models.query_utils import Q

def test_q_init_with_args():
    q = Q('field1', 'field2')
    assert q.children == ['field1', 'field2']
    assert q.connector is None
    assert not q.negated

def test_q_init_with_kwargs():
    q = Q(field1='value1', field2='value2')
    assert sorted(q.children) == sorted([('field1', 'value1'), ('field2', 'value2')])
    assert q.connector is None
    assert not q.negated

def test_q_init_with_connector():
    q = Q('field1', 'field2', _connector='OR')
    assert q.children == ['field1', 'field2']
    assert q.connector == 'OR'
    assert not q.negated

def test_q_init_with_negated():
    q = Q('field1', _negated=True)
    assert q.children == ['field1']
    assert q.connector is None
    assert q.negated

def test_q_init_with_args_kwargs_and_connector():
    q = Q('field1', field2='value2', _connector='AND', _negated=True)
    assert sorted(q.children) == sorted(['field1', ('field2', 'value2')])
    assert q.connector == 'AND'
    assert q.negated