import pytest
from django.contrib.auth.models import User
from django.core import checks
from django.core.exceptions import FieldDoesNotExist
from django.contrib.admin import ModelAdmin


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


@pytest.mark.django_db
def test_check_readonly_fields_item():
    admin_checks = BaseModelAdminChecks()
    user_instance = User.objects.create_user(username='testuser', password='password')

    # Test 1: Field exists on model
    result = admin_checks._check_readonly_fields_item(user_instance, 'username', 'User Username')
    assert result == []

    # Test 2: Field exists on instance
    result = admin_checks._check_readonly_fields_item(user_instance, 'email', 'User Email')
    assert result == []

    # Test 3: Field is callable
    result = admin_checks._check_readonly_fields_item(user_instance, user_instance.get_full_name, 'User Full Name')
    assert result == []

    # Test 4: Field does not exist
    result = admin_checks._check_readonly_fields_item(user_instance, 'nonexistent_field', 'Nonexistent Field')
    assert len(result) == 1
    assert result[0].msg == "The value of 'Nonexistent Field' is not a callable, an attribute of 'User', or an attribute of 'auth.User'."
    assert result[0].id == "admin.E035"