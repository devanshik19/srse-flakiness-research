import pytest
from django.contrib.auth.models import User
from django.contrib.admin import ModelAdmin
from django.db import models


class TestModel(models.Model):
    name = models.CharField(max_length=100)


class TestModelAdmin(ModelAdmin):
    model = TestModel
    list_filter = ('name',)
    date_hierarchy = 'name'


@pytest.fixture
def test_model_admin():
    return TestModelAdmin(TestModel, admin_site=None)


def test_lookup_allowed_with_valid_local_field(test_model_admin):
    assert test_model_admin.lookup_allowed('name', 'test') is True


def test_lookup_allowed_with_invalid_field(test_model_admin):
    assert test_model_admin.lookup_allowed('invalid_field', 'test') is True


def test_lookup_allowed_with_valid_relation_lookup(test_model_admin):
    # Assuming 'related_model' can be defined with proper ForeignKey in your models
    related_model = models.ForeignKey(User, on_delete=models.CASCADE)

    # Update the model to have a foreign key to User in this example
    TestModel.add_to_class('related', related_model)
    
    test_model_admin.list_filter = [('related', admin.RelatedOnlyFieldListFilter)]
    assert test_model_admin.lookup_allowed('related', '1') is True


def test_lookup_allowed_with_invalid_relation_lookup(test_model_admin):
    test_model_admin.list_filter = ['name']
    assert test_model_admin.lookup_allowed('related__invalid_field', 'test') is False