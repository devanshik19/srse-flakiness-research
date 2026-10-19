import pytest
from django.core.exceptions import FieldError
from django.db.models.aggregates import Aggregate

class TestAggregate(Aggregate):
    def __init__(self, distinct=False, filter=None):
        self.distinct = distinct
        self.filter = filter
        super().__init__()

def test_get_repr_options_distinct():
    aggregate = TestAggregate(distinct=True)
    expected_options = {'distinct': True}
    options = aggregate._get_repr_options()
    assert options == expected_options

def test_get_repr_options_filter():
    aggregate = TestAggregate(filter='some_filter_condition')
    expected_options = {'filter': 'some_filter_condition'}
    options = aggregate._get_repr_options()
    assert options == expected_options

def test_get_repr_options_distinct_and_filter():
    aggregate = TestAggregate(distinct=True, filter='some_filter_condition')
    expected_options = {'distinct': True, 'filter': 'some_filter_condition'}
    options = aggregate._get_repr_options()
    assert options == expected_options

def test_get_repr_options_no_distinct_no_filter():
    aggregate = TestAggregate()
    expected_options = {}
    options = aggregate._get_repr_options()
    assert options == expected_options