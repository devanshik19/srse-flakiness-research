import pytest
from django.contrib.admin.utils import flatten
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

@pytest.mark.parametrize(
    "field_name, expected_error",
    [
        ("username", None),  # Valid field
        ("email", None),  # Valid field
        ("non_existent_field", "The value of 'non_existent_field' is not a callable, an attribute of 'User', or an attribute of 'auth.User'."),
        (lambda x: x, None),  # Callable
    ]
)
def test_check_readonly_fields_item(field_name, expected_error):
    user_instance = User(username='testuser', email='test@example.com')
    admin_checks = BaseModelAdminChecks()
    
    label = field_name if isinstance(field_name, str) else 'callable'

    errors = admin_checks._check_readonly_fields_item(user_instance, field_name, label)

    if expected_error is None:
        assert errors == []
    else:
        assert len(errors) == 1
        assert errors[0].msg == expected_error