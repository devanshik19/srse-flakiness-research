import pytest
from django.contrib.auth.models import User
from django.contrib.admin import ModelAdmin
from django.db import models
from django.contrib.admin.filters import SimpleListFilter

class TestModel(models.Model):
    name = models.CharField(max_length=100)

class TestModelAdmin(ModelAdmin):
    list_filter = ['name']
    date_hierarchy = 'date_created'
    model = TestModel

@pytest.mark.parametrize(
    "lookup,value,expected",
    [
        ("name", "test", True),  # Local field lookup
        ("name__exact", "test", True),  # Local field with exact match
        ("nonexistent_field", "test", True),  # Nonexistent field should be allowed
        ("relatedmodel__name", "test", False),  # Assuming no relation exists
    ]
)
def test_lookup_allowed(lookup, value, expected):
    admin = TestModelAdmin(TestModel, admin=None)

    # Mock the necessary attributes and methods for the test
    admin.date_hierarchy = 'date_created'
    admin.list_filter = ['name']

    # Set up the model with related fkey lookups for the test
    admin.model._meta.related_fkey_lookups = []

    assert admin.lookup_allowed(lookup, value) is expected

@pytest.mark.parametrize(
    "lookup,value,expected",
    [
        ("relatedmodel__name", "test", False),  # Non-existent related model
    ]
)
def test_lookup_allowed_with_relationships(lookup, value, expected):
    admin = TestModelAdmin(TestModel, admin=None)

    # Expect certain relationships (mocked)
    admin.model._meta.related_fkey_lookups = [lambda: {}]

    assert admin.lookup_allowed(lookup, value) is expected