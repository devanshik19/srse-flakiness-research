import pytest
from django.core import checks
from django.contrib.auth.models import User
from django.db import models

class TestModel(models.Model):
    class Meta:
        ordering = ['username']  # Change this to test different cases

    username = models.CharField(max_length=100)

def test_check_ordering_valid_ordering():
    meta = TestModel._meta
    assert TestModel._check_ordering() == []

def test_check_ordering_invalid_ordering_type():
    class InvalidOrderingModel(models.Model):
        class Meta:
            ordering = 'username'  # Invalid type (string instead of list/tuple)

    errors = InvalidOrderingModel._check_ordering()
    assert len(errors) == 1
    assert errors[0].id == 'models.E014'

def test_check_ordering_nonexistent_field():
    class NonExistentModel(models.Model):
        class Meta:
            ordering = ['nonexistent_field']  # Valid field that doesn't exist

    errors = NonExistentModel._check_ordering()
    assert len(errors) == 1
    assert errors[0].id == 'models.E015'

def test_check_ordering_related_field():
    class RelatedFieldModel(models.Model):
        related_user = models.ForeignKey(User, on_delete=models.CASCADE)

        class Meta:
            ordering = ['related_user__username']  # Related field ordering

    errors = RelatedFieldModel._check_ordering()
    assert errors == []  # Should be valid

def test_check_ordering_with_clashes():
    class ClashModel(models.Model):
        class Meta:
            ordering = ['username']
            order_with_respect_to = 'another_field'  # Create a clash

    errors = ClashModel._check_ordering()
    assert len(errors) == 1
    assert errors[0].id == 'models.E021'