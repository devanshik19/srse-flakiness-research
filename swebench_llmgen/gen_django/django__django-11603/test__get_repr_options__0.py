import pytest
from django.db.models import Aggregate
from django.contrib.auth.models import User

class TestAggregate(Aggregate):
    def __init__(self, *args, distinct=False, filter=None, **kwargs):
        self.distinct = distinct
        self.filter = filter
        super().__init__(*args, **kwargs)

def test_get_repr_options_distinct():
    aggregate = TestAggregate(distinct=True)
    options = aggregate._get_repr_options()
    assert options['distinct'] is True
    assert 'filter' not in options

def test_get_repr_options_filter():
    aggregate = TestAggregate(filter='some_filter')
    options = aggregate._get_repr_options()
    assert options['filter'] == 'some_filter'
    assert 'distinct' not in options

def test_get_repr_options_distinct_and_filter():
    aggregate = TestAggregate(distinct=True, filter='some_filter')
    options = aggregate._get_repr_options()
    assert options['distinct'] is True
    assert options['filter'] == 'some_filter'

def test_get_repr_options_no_options():
    aggregate = TestAggregate()
    options = aggregate._get_repr_options()
    assert 'distinct' not in options
    assert 'filter' not in options