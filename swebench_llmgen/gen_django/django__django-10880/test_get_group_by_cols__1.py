import pytest
from django.db.models import Aggregate
from django.contrib.auth.models import User

class TestAggregate(Aggregate):
    def get_group_by_cols(self):
        return super().get_group_by_cols()

def test_get_group_by_cols():
    aggregate_instance = TestAggregate()
    result = aggregate_instance.get_group_by_cols()
    assert result == []