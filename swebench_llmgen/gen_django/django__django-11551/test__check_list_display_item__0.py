import pytest
from django.contrib.admin.utils import ModelAdminChecks
from django.contrib.auth.models import User
from django.core import checks
from django.db import models

class TestModelAdminChecks:

    @pytest.fixture
    def admin_checks(self):
        return ModelAdminChecks()

    def test_check_list_display_item_callable(self, admin_checks):
        result = admin_checks._check_list_display_item(User, lambda x: x, "Test Callable")
        assert result == []

    def test_check_list_display_item_attribute(self, admin_checks):
        result = admin_checks._check_list_display_item(User, 'username', "Test Attribute")
        assert result == []

    def test_check_list_display_item_field(self, admin_checks):
        result = admin_checks._check_list_display_item(User, 'email', "Test Field")
        assert result == []

    def test_check_list_display_item_many_to_many(self, admin_checks):
        # Create a ManyToManyField dynamically for testing
        class TestGroup(models.Model):
            users = models.ManyToManyField(User)

        result = admin_checks._check_list_display_item(TestGroup, 'users', "Test ManyToManyField")
        assert len(result) == 1
        assert isinstance(result[0], checks.Error)
        assert result[0].id == 'admin.E109'

    def test_check_list_display_item_invalid(self, admin_checks):
        result = admin_checks._check_list_display_item(User, 'invalid_field', "Test Invalid Field")
        assert len(result) == 1
        assert isinstance(result[0], checks.Error)
        assert result[0].id == 'admin.E108'