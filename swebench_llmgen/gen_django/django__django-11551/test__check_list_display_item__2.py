import pytest
from django.contrib.admin.utils import ModelAdminChecks
from django.contrib.auth.models import User
from django.core import checks
from django.db import models


class MockAdmin:

    def __init__(self, model):
        self.model = model


def test_check_list_display_item_callable():
    admin_obj = MockAdmin(User)
    checks_instance = ModelAdminChecks()
    
    result = checks_instance._check_list_display_item(admin_obj, lambda x: x, 'Test Callable')
    assert result == []


def test_check_list_display_item_attribute_exists():
    admin_obj = MockAdmin(User)
    checks_instance = ModelAdminChecks()
    
    result = checks_instance._check_list_display_item(admin_obj, 'username', 'Username Field')
    assert result == []


def test_check_list_display_item_attribute_does_not_exist():
    admin_obj = MockAdmin(User)
    checks_instance = ModelAdminChecks()
    
    result = checks_instance._check_list_display_item(admin_obj, 'nonexistent_field', 'Nonexistent Field')
    assert len(result) == 1
    assert result[0].id == 'admin.E108'


def test_check_list_display_item_field_exists():
    admin_obj = MockAdmin(User)
    checks_instance = ModelAdminChecks()
    
    result = checks_instance._check_list_display_item(admin_obj, 'email', 'Email Field')
    assert result == []


def test_check_list_display_item_field_is_many_to_many():
    class ManyToManyModel(models.Model):
        users = models.ManyToManyField(User)

    admin_obj = MockAdmin(ManyToManyModel)
    checks_instance = ModelAdminChecks()
    
    result = checks_instance._check_list_display_item(admin_obj, 'users', 'Users Field')
    assert len(result) == 1
    assert result[0].id == 'admin.E109'