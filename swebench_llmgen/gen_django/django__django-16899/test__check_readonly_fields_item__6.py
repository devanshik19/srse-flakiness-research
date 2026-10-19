import pytest
from django.contrib.admin.utils import flatten
from django.contrib.auth.models import User
from django.core import checks
from django.core.exceptions import FieldDoesNotExist
from django.db import models

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

@pytest.fixture
def user_instance():
    return User(username='testuser', email='test@example.com', password='secret').save()

def test_check_readonly_fields_callable(user_instance):
    checks = BaseModelAdminChecks()
    result = checks._check_readonly_fields_item(user_instance, lambda x: x, "Lambda Field")
    assert result == []

def test_check_readonly_fields_attribute(user_instance):
    checks = BaseModelAdminChecks()
    result = checks._check_readonly_fields_item(user_instance, 'username', "Username Field")
    assert result == []

def test_check_readonly_fields_model_attribute(user_instance):
    checks = BaseModelAdminChecks()
    result = checks._check_readonly_fields_item(user_instance, 'email', "Email Field")
    assert result == []

def test_check_readonly_fields_field_does_not_exist(user_instance):
    checks = BaseModelAdminChecks()
    result = checks._check_readonly_fields_item(user_instance, 'non_existing_field', "Non-existing Field")
    assert len(result) == 1
    assert result[0].id == "admin.E035"
    assert "The value of 'Non-existing Field' is not a callable" in str(result[0])