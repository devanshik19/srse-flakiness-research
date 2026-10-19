import pytest
from django.db.models import Aggregate

class TestAggregate(Aggregate):

    def __init__(self, distinct=None, filter=None, **extra):
        self.distinct = distinct
        self.filter = filter
        super().__init__(**extra)

def test_get_repr_options_with_distinct():
    aggregate = TestAggregate(distinct=True)
    options = aggregate._get_repr_options()
    assert options == {'distinct': True}

def test_get_repr_options_with_filter():
    aggregate = TestAggregate(filter='filter_condition')
    options = aggregate._get_repr_options()
    assert options == {'filter': 'filter_condition'}

def test_get_repr_options_with_both_distinct_and_filter():
    aggregate = TestAggregate(distinct=True, filter='filter_condition')
    options = aggregate._get_repr_options()
    assert options == {'distinct': True, 'filter': 'filter_condition'}

def test_get_repr_options_with_no_options():
    aggregate = TestAggregate()
    options = aggregate._get_repr_options()
    assert options == {}