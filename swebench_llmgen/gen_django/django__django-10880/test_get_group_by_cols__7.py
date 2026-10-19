import pytest
from django.contrib.auth.models import User
from django.db.models import Aggregate

class TestAggregate(Aggregate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_group_by_cols(self):
        return []

def test_get_group_by_cols():
    aggregate_instance = TestAggregate()
    result = aggregate_instance.get_group_by_cols()
    assert result == []