import pytest
from django.core.exceptions import FieldError
from django.db.models.expressions import Case, Func, Star, When
from django.db.models.fields import IntegerField
from django.db.models.functions.mixins import FixDurationInputMixin, NumericOutputFieldMixin
from django.contrib.auth.models import User
from django.db.models import Aggregate

class TestAggregate(Aggregate):
    def __init__(self, distinct=False, filter=None, **extra):
        self.distinct = distinct
        self.filter = filter
        super().__init__(**extra)

def test_get_repr_options_distinct():
    aggregate = TestAggregate(distinct=True)
    options = aggregate._get_repr_options()
    assert options['distinct'] is True

def test_get_repr_options_filter():
    aggregate = TestAggregate(filter=Case(When(id=1, then=1), default=0))
    options = aggregate._get_repr_options()
    assert options['filter'] == aggregate.filter

def test_get_repr_options_no_options():
    aggregate = TestAggregate()
    options = aggregate._get_repr_options()
    assert 'distinct' not in options
    assert 'filter' not in options

def test_get_repr_options_both_options():
    aggregate = TestAggregate(distinct=True, filter=Case(When(id=1, then=1), default=0))
    options = aggregate._get_repr_options()
    assert options['distinct'] is True
    assert options['filter'] == aggregate.filter