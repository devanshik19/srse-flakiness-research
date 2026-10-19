import pytest
from django.contrib.auth.models import User
from django.db import models
from django.contrib.admin import ModelAdmin

# Test Model
class TestModel(models.Model):
    name = models.CharField(max_length=100)

# Test Admin
class TestAdmin(ModelAdmin):
    model = TestModel
    list_filter = ['name']
    date_hierarchy = 'id'

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.model._meta.related_fkey_lookups = []

# Test Cases
@pytest.fixture
def test_admin():
    return TestAdmin(TestModel, None)

def test_lookup_allowed_with_local_field(test_admin):
    assert test_admin.lookup_allowed('name', 'test') is True

def test_lookup_allowed_with_relation_field(test_admin):
    # Simulate related field lookups
    related_model = models.Model()
    related_model._meta = type('Meta', (), {'related_fkey_lookups': []})()
    test_admin.model._meta.related_fkey_lookups.append(lambda: {'test_field': 'test_value'})
    assert test_admin.lookup_allowed('test_field', 'test_value') is True

def test_lookup_allowed_with_invalid_field(test_admin):
    assert test_admin.lookup_allowed('invalid_field', 'test') is True

def test_lookup_allowed_with_valid_relation_lookup(test_admin):
    test_admin.list_filter.append(('related_field',))
    assert test_admin.lookup_allowed('related_field', 'test') is True

def test_lookup_allowed_with_valid_complex_relation_lookup(test_admin):
    test_admin.list_filter.append(('outer__inner_field',))
    assert test_admin.lookup_allowed('outer__inner_field', 'test') is True

def test_lookup_allowed_with_invalid_complex_relation_lookup(test_admin):
    assert not test_admin.lookup_allowed('outer__invalid_field', 'test')