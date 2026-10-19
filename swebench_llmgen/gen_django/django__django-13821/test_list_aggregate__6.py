import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Aggregate

def test_list_aggregate():
    # Test aggregate function
    def my_aggregate_func(lst):
        return sum(lst)

    # Create a ListAggregate using the list_aggregate function
    ListAggregate = list_aggregate(my_aggregate_func)

    # Check the base class
    assert issubclass(ListAggregate, list)

    # Create an instance of the ListAggregate
    aggregate_instance = ListAggregate()
    
    # Test step method (list.append)
    aggregate_instance.step(1)
    aggregate_instance.step(2)
    aggregate_instance.step(3)

    # Test the finalization of the aggregate function
    assert aggregate_instance.finalize() == 6  # 1 + 2 + 3

    # Test with an empty list
    empty_instance = ListAggregate()
    assert empty_instance.finalize() == 0  # sum of empty list

    # Test with negative numbers
    negative_instance = ListAggregate()
    negative_instance.step(-1)
    negative_instance.step(-2)
    negative_instance.step(-3)
    assert negative_instance.finalize() == -6  # -1 + -2 + -3