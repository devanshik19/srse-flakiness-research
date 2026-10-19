import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.sqlite3.base import list_aggregate

def test_list_aggregate_functionality():
    # Define a simple aggregation function
    def sum_func(values):
        return sum(values)

    # Create the ListAggregate class with the sum function
    ListAggregate = list_aggregate(sum_func)

    # Create an instance of ListAggregate
    aggregate_instance = ListAggregate()

    # Simulate adding values to the aggregate
    for value in [1, 2, 3, 4, 5]:
        aggregate_instance.step(value)

    # Finalize the aggregation
    result = aggregate_instance.finalize()

    # Assert that the result matches expected output
    assert result == 15  # 1 + 2 + 3 + 4 + 5

def test_list_aggregate_empty():
    # Define a simple aggregation function
    def max_func(values):
        return max(values) if values else None

    # Create the ListAggregate class with the max function
    ListAggregate = list_aggregate(max_func)

    # Create an instance of ListAggregate
    aggregate_instance = ListAggregate()

    # Finalize the aggregation on an empty list
    result = aggregate_instance.finalize()

    # Assert that the result is None for an empty list
    assert result is None