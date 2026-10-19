import pytest
from django.contrib.auth.models import User
from django.db.models import Aggregate

class TestAggregate(Aggregate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_group_by_cols(self):
        return super().get_group_by_cols()

def test_get_group_by_cols():
    aggregate = TestAggregate()
    assert aggregate.get_group_by_cols() == []