import pytest
from django.db.models import Aggregate
from django.contrib.auth.models import User

class TestAggregate:
    def test_get_group_by_cols(self):
        aggregate = Aggregate()
        assert aggregate.get_group_by_cols() == []