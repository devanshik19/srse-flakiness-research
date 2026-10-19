import pytest
from django.core import checks
from django.db import models
from django.contrib.auth.models import User

class TestModel(models.Model):
    ordering = ['username']

class ModelWithErrors(models.Model):
    ordering = ['non_existent_field', 'username']
    order_with_respect_to = 'some_field'

def test_check_ordering_valid_ordering():
    errors = TestModel._check_ordering()
    assert errors == []

def test_check_ordering_invalid_ordering_type():
    class InvalidOrderingType(models.Model):
        ordering = 'username'  # Not a list or tuple

    errors = InvalidOrderingType._check_ordering()
    expected_error = checks.Error(
        "'ordering' must be a tuple or list (even if you want to order by only one field).",
        obj=InvalidOrderingType,
        id='models.E014',
    )
    assert errors == [expected_error]

def test_check_ordering_invalid_field():
    errors = ModelWithErrors._check_ordering()
    expected_error = checks.Error(
        "'ordering' refers to the nonexistent field, related field, or lookup 'non_existent_field'.",
        obj=ModelWithErrors,
        id='models.E015',
    )
    assert errors == [expected_error]

def test_check_ordering_clash():
    class OrderingClash(models.Model):
        ordering = ['username']
        order_with_respect_to = 'profile'

    errors = OrderingClash._check_ordering()
    expected_error = checks.Error(
        "'ordering' and 'order_with_respect_to' cannot be used together.",
        obj=OrderingClash,
        id='models.E021',
    )
    assert errors == [expected_error]

def test_check_ordering_valid_related_field():
    class ValidRelatedField(models.Model):
        username = models.CharField(max_length=150)
        ordering = ['username']

    errors = ValidRelatedField._check_ordering()
    assert errors == []

def test_check_ordering_exclude_pk():
    class ExcludePK(models.Model):
        username = models.CharField(max_length=150)
        ordering = ['pk']  # Should exclude 'pk'

    errors = ExcludePK._check_ordering()
    assert errors == []