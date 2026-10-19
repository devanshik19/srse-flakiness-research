import pytest
from django.db import models
from django.contrib.auth.models import User
from django.core import checks
from django.core.exceptions import FieldDoesNotExist

class BaseModelAdminChecks:
    def _check_readonly_fields_item(self, obj, field_name, label):
        if callable(field_name):
            return []
        elif hasattr(obj, field_name):
            return []
        elif hasattr(obj.model, field_name):
            return []
        else:
            try:
                obj.model._meta.get_field(field_name)
            except FieldDoesNotExist:
                return [
                    checks.Error(
                        "The value of '%s' is not a callable, an attribute of "
                        "'%s', or an attribute of '%s'."
                        % (
                            label,
                            obj.__class__.__name__,
                            obj.model._meta.label,
                        ),
                        obj=obj.__class__,
                        id="admin.E035",
                    )
                ]
            else:
                return []

class TestBaseModelAdminChecks:
    
    @pytest.fixture
    def admin_checks(self):
        return BaseModelAdminChecks()

    @pytest.fixture
    def user_instance(self):
        return User(username='testuser', email='test@example.com')

    def test_readonly_field_callable(self, admin_checks, user_instance):
        result = admin_checks._check_readonly_fields_item(user_instance, lambda: None, 'Test Callable')
        assert result == []

    def test_readonly_field_has_attribute(self, admin_checks, user_instance):
        result = admin_checks._check_readonly_fields_item(user_instance, 'username', 'Username')
        assert result == []

    def test_readonly_field_has_model_attribute(self, admin_checks, user_instance):
        result = admin_checks._check_readonly_fields_item(user_instance, 'email', 'Email')
        assert result == []

    def test_readonly_field_field_does_not_exist(self, admin_checks, user_instance):
        result = admin_checks._check_readonly_fields_item(user_instance, 'non_existent_field', 'Non Existent Field')
        assert len(result) == 1
        assert result[0].id == "admin.E035"
        assert "The value of 'Non Existent Field' is not a callable, an attribute of 'User', or an attribute of 'auth.User'." in str(result[0])