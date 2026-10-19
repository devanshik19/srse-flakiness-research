import pytest
from django.core import checks
from django.db import models
from django.db.models import Lookup

class TestModel(models.Model):
    field_one = models.CharField(max_length=100)
    field_two = models.IntegerField()

    class Meta:
        ordering = ['field_one']

def test_check_ordering_with_valid_fields():
    errors = TestModel._check_ordering()
    assert len(errors) == 0

def test_check_ordering_with_invalid_field():
    class InvalidModel(models.Model):
        field_one = models.CharField(max_length=100)

        class Meta:
            ordering = ['invalid_field']

    errors = InvalidModel._check_ordering()
    assert len(errors) == 1
    assert errors[0].id == 'models.E015'

def test_check_ordering_with_non_list_ordering():
    class NonListModel(models.Model):
        field_one = models.CharField(max_length=100)

        class Meta:
            ordering = 'field_one'

    errors = NonListModel._check_ordering()
    assert len(errors) == 1
    assert errors[0].id == 'models.E014'

def test_check_ordering_with_ordering_and_order_with_respect_to():
    class ClashModel(models.Model):
        field_one = models.CharField(max_length=100)

        class Meta:
            ordering = ['field_one']
            order_with_respect_to = 'field_one'

    errors = ClashModel._check_ordering()
    assert len(errors) == 1
    assert errors[0].id == 'models.E021'

def test_check_ordering_with_related_field():
    class RelatedModel(models.Model):
        field_one = models.CharField(max_length=100)

    class ModelWithRelation(models.Model):
        related_model = models.ForeignKey(RelatedModel, on_delete=models.CASCADE)

        class Meta:
            ordering = ['related_model__field_one']

    errors = ModelWithRelation._check_ordering()
    assert len(errors) == 0

def test_check_ordering_with_invalid_related_field():
    class InvalidRelationModel(models.Model):
        related_model = models.ForeignKey('NonExistentModel', on_delete=models.CASCADE)

        class Meta:
            ordering = ['related_model__invalid_field']

    errors = InvalidRelationModel._check_ordering()
    assert len(errors) == 1
    assert errors[0].id == 'models.E015'