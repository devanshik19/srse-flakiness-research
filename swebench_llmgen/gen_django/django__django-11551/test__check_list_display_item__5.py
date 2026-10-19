import pytest
from django.contrib.admin.utils import ModelAdminChecks
from django.core import checks
from django.core.exceptions import FieldDoesNotExist
from django.contrib.auth.models import User

class TestModelAdminChecks:

    @pytest.fixture
    def model_admin_checks(self):
        return ModelAdminChecks()

    def test_check_list_display_item_callable(self, model_admin_checks):
        obj = User
        item = lambda x: x
        label = 'test_label'
        result = model_admin_checks._check_list_display_item(obj, item, label)
        assert result == []

    def test_check_list_display_item_has_attribute(self, model_admin_checks):
        obj = User
        item = 'username'
        label = 'test_label'
        result = model_admin_checks._check_list_display_item(obj, item, label)
        assert result == []

    def test_check_list_display_item_field_exists(self, model_admin_checks):
        obj = User
        item = 'email'
        label = 'test_label'
        result = model_admin_checks._check_list_display_item(obj, item, label)
        assert result == []

    def test_check_list_display_item_field_does_not_exist(self, model_admin_checks):
        obj = User
        item = 'nonexistent_field'
        label = 'test_label'
        result = model_admin_checks._check_list_display_item(obj, item, label)
        assert len(result) == 1
        assert result[0].id == 'admin.E108'

    def test_check_list_display_item_many_to_many_field(self, model_admin_checks):
        class CustomUser(User):
            groups = []  # Simulate ManyToManyField

        obj = CustomUser
        item = 'groups'
        label = 'test_label'
        result = model_admin_checks._check_list_display_item(obj, item, label)
        assert len(result) == 1
        assert result[0].id == 'admin.E109'