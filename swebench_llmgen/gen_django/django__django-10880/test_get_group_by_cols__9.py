import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db.models import Aggregate

class TestAggregate(Aggregate):
    def get_group_by_cols(self):
        return []

@pytest.mark.django_db
def test_get_group_by_cols():
    aggregate_instance = TestAggregate()
    group_by_cols = aggregate_instance.get_group_by_cols()
    
    assert group_by_cols == []