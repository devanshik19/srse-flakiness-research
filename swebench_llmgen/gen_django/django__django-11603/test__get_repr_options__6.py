import pytest
from django.db.models.aggregates import Aggregate
from django.db.models.expressions import Case, When
from django.core.exceptions import FieldError
from django.db.models.fields import IntegerField

class TestAggregate(Aggregate):
    def __init__(self, distinct=False, filter=None, *args, **kwargs):
        self.distinct = distinct
        self.filter = filter
        super().__init__(*args, **kwargs)

def test_get_repr_options_no_distinct_no_filter():
    agg = TestAggregate()
    options = agg._get_repr_options()
    assert options == {}

def test_get_repr_options_with_distinct():
    agg = TestAggregate(distinct=True)
    options = agg._get_repr_options()
    assert options == {'distinct': True}

def test_get_repr_options_with_filter():
    agg = TestAggregate(filter=Case(When(id=1, then=1)))
    options = agg._get_repr_options()
    assert options == {'filter': agg.filter}

def test_get_repr_options_with_distinct_and_filter():
    agg = TestAggregate(distinct=True, filter=Case(When(id=1, then=1)))
    options = agg._get_repr_options()
    assert options == {'distinct': True, 'filter': agg.filter}