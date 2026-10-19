import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import FieldDoesNotExist
from django.contrib.admin.filters import SimpleListFilter


class TestModel(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)

class Department(models.Model):
    name = models.CharField(max_length=100)


class BaseModelAdminTest(ModelAdmin):
    model = TestModel
    list_filter = ['name', ('department', SimpleListFilter)]
    date_hierarchy = 'name'


@pytest.fixture
def base_model_admin():
    return BaseModelAdminTest(TestModel, None)


def test_lookup_allowed_with_local_field(base_model_admin):
    assert base_model_admin.lookup_allowed('name', 'John Doe') is True


def test_lookup_allowed_with_valid_relation(base_model_admin):
    assert base_model_admin.lookup_allowed('department', 1) is True


def test_lookup_allowed_with_valid_nested_relation(base_model_admin):
    assert base_model_admin.lookup_allowed('department__name', 'IT') is True


def test_lookup_allowed_with_invalid_field(base_model_admin):
    assert base_model_admin.lookup_allowed('invalid_field', 'value') is True


def test_lookup_allowed_with_non_relatable_field(base_model_admin):
    result = base_model_admin.lookup_allowed('name__invalid', 'value')
    assert result is True


def test_lookup_allowed_with_nested_non_relatable_field(base_model_admin):
    result = base_model_admin.lookup_allowed('department__non_existent_field', 'value')
    assert result is True


def test_lookup_allowed_for_unsupported_relation(base_model_admin):
    base_model_admin.list_filter = ['name', 'unknown_field']
    assert base_model_admin.lookup_allowed('unknown_field', 'value') is False