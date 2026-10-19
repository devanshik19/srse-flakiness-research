import pytest
from django.db.models.query_utils import Q

def test_q_init_with_args():
    q_instance = Q('field1', 'field2')
    assert q_instance.children == ['field1', 'field2']
    assert q_instance.connector is None
    assert not q_instance.negated

def test_q_init_with_kwargs():
    q_instance = Q(field1='value1', field2='value2')
    assert q_instance.children == ['field1', 'value1', 'field2', 'value2']
    assert q_instance.connector is None
    assert not q_instance.negated

def test_q_init_with_connector_and_negated():
    q_instance = Q('field1', _connector='AND', _negated=True)
    assert q_instance.children == ['field1']
    assert q_instance.connector == 'AND'
    assert q_instance.negated

def test_q_init_with_empty():
    q_instance = Q()
    assert q_instance.children == []
    assert q_instance.connector is None
    assert not q_instance.negated