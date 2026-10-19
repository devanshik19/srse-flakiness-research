import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.sqlite3.base import list_aggregate

def test_list_aggregate():
    # Define a simple aggregation function to use with list_aggregate
    def sum_aggregate(values):
        return sum(values)

    # Create an aggregate class
    ListSum = list_aggregate(sum_aggregate)

    # Instantiate the list aggregate
    aggregate_instance = ListSum()

    # Simulate the step function
    aggregate_instance.step(10)
    aggregate_instance.step(20)
    aggregate_instance.step(30)

    # Check the contents of the list
    assert aggregate_instance == [10, 20, 30]

    # Finalize the aggregate and check if the sum is correct
    result = aggregate_instance.finalize()
    assert result == 60

    # Test with an empty list
    empty_instance = ListSum()
    empty_result = empty_instance.finalize()
    assert empty_result == 0