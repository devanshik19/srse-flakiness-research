import pytest
from django.db.models import Q
from django.contrib.auth.models import User

def test_q_init_with_args():
    # Test Q initialization with positional arguments
    q1 = Q('field1', 'field2')
    assert q1.children == ['field1', 'field2']  # expectation based on positional args
    assert q1.connector is None
    assert not q1.negated

def test_q_init_with_kwargs():
    # Test Q initialization with keyword arguments
    q2 = Q(field1='value1', field2='value2')
    assert q2.children == [('field1', 'value1'), ('field2', 'value2')]  # expectation based on kwargs
    assert q2.connector is None
    assert not q2.negated

def test_q_init_with_connector_and_negation():
    # Test Q initialization with connector and negation
    q3 = Q('field1', _connector='OR', _negated=True)
    assert q3.children == ['field1']
    assert q3.connector == 'OR'
    assert q3.negated

def test_q_init_empty():
    # Test Q initialization with no arguments
    q4 = Q()
    assert q4.children == []  # expectation for no positional or keyword args
    assert q4.connector is None
    assert not q4.negated