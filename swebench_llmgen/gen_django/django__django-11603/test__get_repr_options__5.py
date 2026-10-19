import pytest
from django.db.models import Aggregate
from django.contrib.auth.models import User

class MockAggregate(Aggregate):
    def __init__(self, distinct=False, filter=None):
        self.distinct = distinct
        self.filter = filter
        super().__init__()

def test_get_repr_options_distinct():
    agg = MockAggregate(distinct=True)
    options = agg._get_repr_options()
    assert options['distinct'] is True
    assert 'filter' not in options

def test_get_repr_options_filter():
    agg = MockAggregate(filter='some_filter')
    options = agg._get_repr_options()
    assert options['filter'] == 'some_filter'
    assert 'distinct' not in options

def test_get_repr_options_both():
    agg = MockAggregate(distinct=True, filter='some_filter')
    options = agg._get_repr_options()
    assert options['distinct'] is True
    assert options['filter'] == 'some_filter'

def test_get_repr_options_neither():
    agg = MockAggregate()
    options = agg._get_repr_options()
    assert 'distinct' not in options
    assert 'filter' not in options