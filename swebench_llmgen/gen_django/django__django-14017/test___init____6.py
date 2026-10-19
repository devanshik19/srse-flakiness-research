import pytest
from django.db.models.query_utils import Q


def test_q_init_with_args():
    q_instance = Q('field1', 'field2')
    assert isinstance(q_instance, Q)
    assert q_instance.children == ['field1', 'field2']


def test_q_init_with_kwargs():
    q_instance = Q(field1='value1', field2='value2')
    assert isinstance(q_instance, Q)
    assert q_instance.children == [('field1', 'value1'), ('field2', 'value2')]
    

def test_q_init_with_connector():
    q_instance = Q('field1', _connector='OR')
    assert isinstance(q_instance, Q)
    assert q_instance.children == ['field1']
    assert q_instance.connector == 'OR'


def test_q_init_with_negation():
    q_instance = Q('field1', _negated=True)
    assert isinstance(q_instance, Q)
    assert q_instance.children == ['field1']
    assert q_instance.negated is True


def test_q_init_with_mixed_args_and_kwargs():
    q_instance = Q('field1', field2='value2')
    assert isinstance(q_instance, Q)
    assert q_instance.children == ['field1', ('field2', 'value2')]