import pytest
from django.db.models import Aggregate
from django.contrib.auth.models import User


class CustomAggregate(Aggregate):
    def __init__(self, distinct=False, filter=None, *args, **kwargs):
        self.distinct = distinct
        self.filter = filter
        super().__init__(*args, **kwargs)


def test_get_repr_options_distinct():
    aggregate = CustomAggregate(distinct=True)
    options = aggregate._get_repr_options()
    assert options['distinct'] is True


def test_get_repr_options_filter():
    aggregate = CustomAggregate(filter='some_filter')
    options = aggregate._get_repr_options()
    assert options['filter'] == 'some_filter'


def test_get_repr_options_no_distinct_no_filter():
    aggregate = CustomAggregate()
    options = aggregate._get_repr_options()
    assert 'distinct' not in options
    assert 'filter' not in options


def test_get_repr_options_distinct_and_filter():
    aggregate = CustomAggregate(distinct=True, filter='some_filter')
    options = aggregate._get_repr_options()
    assert options['distinct'] is True
    assert options['filter'] == 'some_filter'