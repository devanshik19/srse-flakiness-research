import pytest
from django.contrib.auth.models import User
from django.db.models import Aggregate

class CustomAggregate(Aggregate):
    def get_group_by_cols(self):
        return super().get_group_by_cols()

def test_get_group_by_cols():
    custom_aggregate = CustomAggregate()

    # Ensure that get_group_by_cols returns an empty list
    result = custom_aggregate.get_group_by_cols()
    assert result == []