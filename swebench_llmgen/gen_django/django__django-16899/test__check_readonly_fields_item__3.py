import pytest
from django.contrib.auth.models import User
from django.core import checks
from django.core.exceptions import FieldDoesNotExist
from django.db import models


class TestBaseModelAdminChecks:

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

    def test_readonly_fields_item_callable(self):
        admin_checks = self.BaseModelAdminChecks()
        result = admin_checks._check_readonly_fields_item(User, lambda x: x, "User Field")
        assert result == []

    def test_readonly_fields_item_has_attribute(self):
        admin_checks = self.BaseModelAdminChecks()
        user_instance = User(username='test')
        result = admin_checks._check_readonly_fields_item(user_instance, 'username', "User Field")
        assert result == []

    def test_readonly_fields_item_has_model_attribute(self):
        admin_checks = self.BaseModelAdminChecks()
        result = admin_checks._check_readonly_fields_item(User, 'username', "User Field")
        assert result == []

    def test_readonly_fields_item_field_does_not_exist(self):
        admin_checks = self.BaseModelAdminChecks()
        user_instance = User(username='test')
        result = admin_checks._check_readonly_fields_item(user_instance, 'non_existent_field', "User Field")
        assert len(result) == 1
        assert result[0].id == "admin.E035"
        assert "non_existent_field" in str(result[0])