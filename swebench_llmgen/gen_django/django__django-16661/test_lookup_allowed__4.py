import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import FieldDoesNotExist

class TestModel(models.Model):
    name = models.CharField(max_length=100)

class TestAdmin(ModelAdmin):
    model = TestModel
    list_filter = ['name']

    @property
    def date_hierarchy(self):
        return 'date_created'

@pytest.mark.django_db
def test_lookup_allowed_with_valid_lookup(monkeypatch):
    admin = TestAdmin(TestModel, admin_site=None)
    
    # Define fake related lookups
    def related_fkey_lookups(*args, **kwargs):
        return [admin.date_hierarchy]

    monkeypatch.setattr(TestModel._meta, 'related_fkey_lookups', related_fkey_lookups)

    assert admin.lookup_allowed('name', 'test') is True  # Local field
    assert admin.lookup_allowed('date_created', '2023-01-01') is True  # Valid date field

def test_lookup_allowed_with_invalid_lookup():
    admin = TestAdmin(TestModel, admin_site=None)
    
    # The field is not defined in TestModel
    with pytest.raises(FieldDoesNotExist):
        assert admin.lookup_allowed('invalid_field', 'test')

def test_lookup_allowed_with_relationship(monkeypatch):
    admin = TestAdmin(TestModel, admin_site=None)

    # Create a fake field where path_infos is defined
    class RelatedField:
        is_relation = True
        path_infos = [{'target_fields': [models.CharField(max_length=100)]}]
    
    monkeypatch.setattr(TestModel._meta, 'get_field', lambda field_name: RelatedField() if field_name == 'related_field' else None)

    assert admin.lookup_allowed('related_field', 'test') is True  # Valid relationship lookup