import pytest
from django.db.models.aggregates import Aggregate
from django.contrib.auth.models import User

class TestAggregate:

    def test_get_group_by_cols(self):
        aggregate_instance = Aggregate()
        result = aggregate_instance.get_group_by_cols()
        assert result == []