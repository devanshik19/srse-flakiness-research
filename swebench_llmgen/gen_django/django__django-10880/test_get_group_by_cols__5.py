import pytest
from django.db.models import Aggregate
from django.contrib.auth.models import User

class TestAggregate(Aggregate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def test_get_group_by_cols():
    aggregate = TestAggregate()
    result = aggregate.get_group_by_cols()
    assert result == []