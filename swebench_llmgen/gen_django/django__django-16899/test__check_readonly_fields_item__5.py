import pytest
from django.contrib.admin.checks import BaseModelAdminChecks
from django.core import checks
from django.contrib.auth.models import User
from django.core.exceptions import FieldDoesNotExist

class TestBaseModelAdminChecks:

    @pytest.fixture
    def admin_checks(self):
        return BaseModelAdminChecks()

    def test_check_readonly_fields_item_callable(self, admin_checks):
        result = admin_checks._check_readonly_fields_item(User, User.username, 'username')
        assert result == []

    def test_check_readonly_fields_item_attribute(self, admin_checks):
        result = admin_checks._check_readonly_fields_item(User(), 'username', 'username')
        assert result == []

    def test_check_readonly_fields_item_model_attribute(self, admin_checks):
        result = admin_checks._check_readonly_fields_item(User(), 'objects', 'objects')
        assert result == []

    def test_check_readonly_fields_item_field_does_not_exist(self, admin_checks):
        result = admin_checks._check_readonly_fields_item(User(), 'non_existent_field', 'non_existent_field')
        assert len(result) == 1
        assert isinstance(result[0], checks.Error)
        assert "The value of 'non_existent_field' is not a callable" in str(result[0])