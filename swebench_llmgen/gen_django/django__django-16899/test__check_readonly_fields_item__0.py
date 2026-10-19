import pytest
from django.contrib.admin.checks import BaseModelAdminChecks
from django.contrib.auth.models import User
from django.core import checks
from django.core.exceptions import FieldDoesNotExist

class TestBaseModelAdminChecks:

    @pytest.fixture
    def checks_instance(self):
        return BaseModelAdminChecks()

    def test_check_readonly_fields_item_callable(self, checks_instance):
        result = checks_instance._check_readonly_fields_item(User, 'username', 'Username')
        assert result == []

    def test_check_readonly_fields_item_attribute(self, checks_instance):
        result = checks_instance._check_readonly_fields_item(User, 'id', 'User ID')
        assert result == []

    def test_check_readonly_fields_item_model_attribute(self, checks_instance):
        result = checks_instance._check_readonly_fields_item(User, 'is_active', 'Is Active')
        assert result == []

    def test_check_readonly_fields_item_field_does_not_exist(self, checks_instance):
        result = checks_instance._check_readonly_fields_item(User, 'non_existing_field', 'Non Existing Field')
        assert len(result) == 1
        assert isinstance(result[0], checks.Error)
        assert "The value of 'Non Existing Field' is not a callable, an attribute of" in str(result[0])