import pytest
from django.db.models import Aggregate

class TestAggregate(Aggregate):
    def __init__(self, distinct=None, filter=None, **extra):
        self.distinct = distinct
        self.filter = filter
        super().__init__(**extra)

def test_get_repr_options_with_distinct_and_filter():
    aggregate = TestAggregate(distinct=True, filter='some_filter')
    options = aggregate._get_repr_options()
    assert options == {'distinct': True, 'filter': 'some_filter'}

def test_get_repr_options_with_distinct_only():
    aggregate = TestAggregate(distinct=True)
    options = aggregate._get_repr_options()
    assert options == {'distinct': True}

def test_get_repr_options_with_filter_only():
    aggregate = TestAggregate(filter='some_filter')
    options = aggregate._get_repr_options()
    assert options == {'filter': 'some_filter'}

def test_get_repr_options_without_distinct_or_filter():
    aggregate = TestAggregate()
    options = aggregate._get_repr_options()
    assert options == {}