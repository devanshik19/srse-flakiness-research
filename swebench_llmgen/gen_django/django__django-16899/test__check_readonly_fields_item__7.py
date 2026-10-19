import collections
from django.contrib.admin.utils import NotRelationField
from django.core import checks
from django.core.exceptions import FieldDoesNotExist
from django.contrib.auth.models import User


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


def test_check_readonly_fields_item():
    checks_instance = BaseModelAdminChecks()
    user = User(username='testuser')
    
    # Test callable field_name
    assert checks_instance._check_readonly_fields_item(user, lambda: None, 'Callable Field') == []
    
    # Test attribute of instance
    assert checks_instance._check_readonly_fields_item(user, 'username', 'Username field') == []
    
    # Test attribute of model
    assert checks_instance._check_readonly_fields_item(user, 'email', 'Email field') == []
    
    # Test non-existent field causing FieldDoesNotExist
    errors = checks_instance._check_readonly_fields_item(user, 'non_existent_field', 'Non-existent field')
    assert len(errors) == 1
    assert errors[0].msg == "The value of 'Non-existent field' is not a callable, an attribute of 'User', or an attribute of 'auth.User'."
    assert errors[0].id == "admin.E035"