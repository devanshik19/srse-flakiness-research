import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.db import models
from django.contrib.admin.filters import SimpleListFilter

class TestModel(models.Model):
    name = models.CharField(max_length=100)
    related_field = models.ForeignKey(User, on_delete=models.CASCADE)

class TestModelAdmin(ModelAdmin):
    model = TestModel
    list_filter = ['related_field']

def test_lookup_allowed_with_local_field():
    admin = TestModelAdmin(TestModel, admin.site)
    assert admin.lookup_allowed('name', 'test') is True

def test_lookup_allowed_with_related_field():
    admin = TestModelAdmin(TestModel, admin.site)
    assert admin.lookup_allowed('related_field', 1) is True

def test_lookup_allowed_with_invalid_field():
    admin = TestModelAdmin(TestModel, admin.site)
    assert admin.lookup_allowed('invalid_field', 'test') is True

def test_lookup_allowed_with_relation_filter():
    admin = TestModelAdmin(TestModel, admin.site)
    assert admin.lookup_allowed('related_field__isnull', True) is True

def test_lookup_allowed_with_non_relatable_field():
    admin = TestModelAdmin(TestModel, admin.site)
    admin.list_filter = [SimpleListFilter]
    assert admin.lookup_allowed('related_field__relatedfield', 1) is False