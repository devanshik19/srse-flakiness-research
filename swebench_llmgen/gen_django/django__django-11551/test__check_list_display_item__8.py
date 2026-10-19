import pytest
from django.contrib.admin.utils import ModelAdminChecks
from django.contrib.auth.models import User
from django.core import checks

class FakeAdmin:
    model = User

def test_check_list_display_item_callable():
    checker = ModelAdminChecks()
    result = checker._check_list_display_item(FakeAdmin(), lambda x: x, "Test Item")
    assert result == []

def test_check_list_display_item_attribute_exists():
    checker = ModelAdminChecks()
    result = checker._check_list_display_item(FakeAdmin(), 'username', "Username")
    assert result == []

def test_check_list_display_item_field_exists():
    checker = ModelAdminChecks()
    result = checker._check_list_display_item(FakeAdmin(), 'first_name', "First Name")
    assert result == []

def test_check_list_display_item_field_does_not_exist():
    checker = ModelAdminChecks()
    result = checker._check_list_display_item(FakeAdmin(), 'nonexistent_field', "Nonexistent Field")
    assert len(result) == 1
    assert result[0].id == 'admin.E108'

def test_check_list_display_item_many_to_many_field():
    class Group(models.Model):
        name = models.CharField(max_length=100)

    class UserWithManyToMany:
        model = User
        groups = models.ManyToManyField(Group)

    checker = ModelAdminChecks()
    result = checker._check_list_display_item(UserWithManyToMany(), 'groups', "Groups")
    assert len(result) == 1
    assert result[0].id == 'admin.E109'

def test_check_list_display_item_attribute_of_model():
    checker = ModelAdminChecks()
    result = checker._check_list_display_item(FakeAdmin(), 'is_active', "Is Active")
    assert result == []