import pytest
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import list_aggregate

def sum_values(values):
    return sum(values)

def test_list_aggregate():
    # Create an instance of the aggregate function
    ListSum = list_aggregate(sum_values)

    # Create an instance of the ListSum
    aggregate_instance = ListSum()

    # Test step method
    aggregate_instance.step(1)
    aggregate_instance.step(2)
    aggregate_instance.step(3)

    # Verify that values are stored correctly
    assert len(aggregate_instance) == 3
    assert aggregate_instance[0] == 1
    assert aggregate_instance[1] == 2
    assert aggregate_instance[2] == 3

    # Test finalize method
    result = aggregate_instance.finalize()
    assert result == 6  # 1 + 2 + 3 = 6

    # Test edge case with no values
    empty_instance = ListSum()
    assert empty_instance.finalize() == 0  # No values to sum

    # Test with negative values
    negate_sum = list_aggregate(lambda values: sum(values))
    negative_instance = negate_sum()
    negative_instance.step(-1)
    negative_instance.step(-2)
    negative_instance.step(-3)
    assert negative_instance.finalize() == -6  # -1 + -2 + -3 = -6