import pytest
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import list_aggregate

def test_list_aggregate_sum():
    """Test list_aggregate with sum function."""
    aggregate = list_aggregate(sum)
    values = aggregate()
    values.step(1)
    values.step(2)
    values.step(3)
    result = values.finalize()
    assert result == 6

def test_list_aggregate_max():
    """Test list_aggregate with max function."""
    aggregate = list_aggregate(max)
    values = aggregate()
    values.step(4)
    values.step(2)
    values.step(7)
    result = values.finalize()
    assert result == 7

def test_list_aggregate_min():
    """Test list_aggregate with min function."""
    aggregate = list_aggregate(min)
    values = aggregate()
    values.step(20)
    values.step(5)
    values.step(15)
    result = values.finalize()
    assert result == 5

def test_list_aggregate_empty():
    """Test list_aggregate with empty list."""
    aggregate = list_aggregate(sum)
    values = aggregate()
    result = values.finalize()
    assert result == 0