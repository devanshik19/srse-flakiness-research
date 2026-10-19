import pytest
from django.contrib.admin.utils import ModelAdminChecks
from django.contrib.auth.models import User
from django.core import checks
from django.db import models

class MockAdmin:
    def __init__(self, model):
        self.model = model

def test_check_list_display_item_callable():
    admin = MockAdmin(User)
    checks_instance = ModelAdminChecks()
    result = checks_instance._check_list_display_item(admin, lambda x: x, 'test_label')
    assert result == []

def test_check_list_display_item_attribute():
    admin = MockAdmin(User)
    checks_instance = ModelAdminChecks()
    result = checks_instance._check_list_display_item(admin, 'username', 'test_label')
    assert result == []

def test_check_list_display_item_model_field():
    admin = MockAdmin(User)
    checks_instance = ModelAdminChecks()
    result = checks_instance._check_list_display_item(admin, 'date_joined', 'test_label')
    assert result == []

def test_check_list_display_item_many_to_many_field():
    class TestModel(models.Model):
        groups = models.ManyToManyField(User)

    admin = MockAdmin(TestModel)
    checks_instance = ModelAdminChecks()
    result = checks_instance._check_list_display_item(admin, 'groups', 'test_label')
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].id == 'admin.E109'

def test_check_list_display_item_invalid_attribute():
    admin = MockAdmin(User)
    checks_instance = ModelAdminChecks()
    result = checks_instance._check_list_display_item(admin, 'invalid_field', 'test_label')
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].id == 'admin.E108'