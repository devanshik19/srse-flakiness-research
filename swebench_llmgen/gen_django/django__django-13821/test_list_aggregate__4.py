import pytest
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import list_aggregate

def test_list_aggregate():
    # A simple function to use for finalizing the aggregates
    def sum_values(lst):
        return sum(lst)

    # Create the list aggregate using the helper function
    ListAggregate = list_aggregate(sum_values)

    # Simulate the steps of the aggregation
    aggregated = ListAggregate()
    aggregated.step(1)
    aggregated.step(2)
    aggregated.step(3)

    # Finalize the aggregate and check if it gives the correct result
    result = aggregated.finalize()
    assert result == 6, "Expected sum of values to be 6"

    # Testing with an empty ListAggregate
    empty_aggregate = ListAggregate()
    result_empty = empty_aggregate.finalize()
    assert result_empty == 0, "Expected sum of empty aggregate to be 0"

    # Testing another function - finding the average
    def average_values(lst):
        return statistics.mean(lst) if lst else 0

    AverageAggregate = list_aggregate(average_values)
    avg_aggregate = AverageAggregate()
    avg_aggregate.step(4)
    avg_aggregate.step(8)

    avg_result = avg_aggregate.finalize()
    assert avg_result == 6, "Expected average of values to be 6"