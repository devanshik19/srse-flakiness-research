import pytest
from django.contrib.admin.checks import BaseModelAdminChecks
from django.contrib.auth.models import User
from django.core import checks
from django.core.exceptions import FieldDoesNotExist

class TestBaseModelAdminChecks:

    @pytest.fixture
    def checks_instance(self):
        return BaseModelAdminChecks()

    def test_callable_field(self, checks_instance):
        assert checks_instance._check_readonly_fields_item(User(), lambda x: x, "Test Callable") == []

    def test_attribute_exists(self, checks_instance):
        assert checks_instance._check_readonly_fields_item(User(username='testuser'), 'username', "Username") == []

    def test_model_attribute_exists(self, checks_instance):
        assert checks_instance._check_readonly_fields_item(User(), 'is_active', "Is Active") == []

    def test_field_does_not_exist(self, checks_instance):
        errors = checks_instance._check_readonly_fields_item(User(), 'non_existent_field', "Non Existent Field")
        assert len(errors) == 1
        assert isinstance(errors[0], checks.Error)
        assert "The value of 'Non Existent Field' is not a callable, an attribute of 'User', or an attribute of" in str(errors[0])
        assert errors[0].id == "admin.E035"