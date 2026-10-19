import pytest
from django.db.models.aggregates import Aggregate

class TestAggregate(Aggregate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def test_get_group_by_cols():
    aggregate_instance = TestAggregate()
    result = aggregate_instance.get_group_by_cols()
    assert result == []