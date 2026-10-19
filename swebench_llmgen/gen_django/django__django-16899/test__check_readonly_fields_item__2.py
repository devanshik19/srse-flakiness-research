import pytest
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
def admin_checks():
    return BaseModelAdminChecks()

def test_check_readonly_fields_item_callable(admin_checks):
    user = User(username='testuser')
    result = admin_checks._check_readonly_fields_item(user, lambda: True, 'my_field')
    assert result == []

def test_check_readonly_fields_item_attribute(admin_checks):
    user = User(username='testuser')
    result = admin_checks._check_readonly_fields_item(user, 'username', 'my_field')
    assert result == []

def test_check_readonly_fields_item_related_field_exist(admin_checks):
    user = User(username='testuser')
    result = admin_checks._check_readonly_fields_item(user, 'id', 'my_field')
    assert result == []

def test_check_readonly_fields_item_field_does_not_exist(admin_checks):
    user = User(username='testuser')
    result = admin_checks._check_readonly_fields_item(user, 'non_existent_field', 'my_field')
    assert len(result) == 1
    assert result[0].id == "admin.E035"