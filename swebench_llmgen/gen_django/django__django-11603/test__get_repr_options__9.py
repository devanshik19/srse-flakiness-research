import pytest
from django.core.exceptions import FieldError
from django.db.models.expressions import Case, Func, Star, When
from django.db.models.fields import IntegerField
from django.db.models.functions.mixins import (
    FixDurationInputMixin, NumericOutputFieldMixin,
)
from django.contrib.auth.models import User

class TestAggregate(Aggregate):
    def __init__(self, distinct=False, filter=None):
        self.distinct = distinct
        self.filter = filter

    def _get_repr_options(self):
        options = super()._get_repr_options()
        if self.distinct:
            options['distinct'] = self.distinct
        if self.filter:
            options['filter'] = self.filter
        return options

def test_get_repr_options_without_distinct_or_filter():
    aggregate = TestAggregate()
    options = aggregate._get_repr_options()
    assert options == {}

def test_get_repr_options_with_distinct():
    aggregate = TestAggregate(distinct=True)
    options = aggregate._get_repr_options()
    assert options == {'distinct': True}

def test_get_repr_options_with_filter():
    aggregate = TestAggregate(filter='my_filter')
    options = aggregate._get_repr_options()
    assert options == {'filter': 'my_filter'}

def test_get_repr_options_with_distinct_and_filter():
    aggregate = TestAggregate(distinct=True, filter='my_filter')
    options = aggregate._get_repr_options()
    assert options == {'distinct': True, 'filter': 'my_filter'}