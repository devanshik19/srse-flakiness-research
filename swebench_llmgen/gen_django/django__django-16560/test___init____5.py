import pytest
from django.core.exceptions import ValidationError
from django.utils.deprecation import RemovedInDjango60Warning
from django.contrib.auth.models import User
from django.db.models import BaseConstraint

@pytest.mark.parametrize(
    "args, name, violation_error_message, expected_error",
    [
        ([], None, None, TypeError),  # Missing required keyword-only argument
        ([], "test_constraint", None, None),  # Valid case with only name
        ([], None, "Custom error message", None),  # Valid case with only violation_error_message
        (["arg_value"], None, None, RemovedInDjango60Warning),  # Deprecation warning with positional arg
    ]
)
def test_base_constraint_init(args, name, violation_error_message, expected_error, caplog):
    if expected_error:
        with pytest.raises(expected_error):
            BaseConstraint(*args, name=name, violation_error_message=violation_error_message)
    else:
        constraint = BaseConstraint(*args, name=name, violation_error_message=violation_error_message)
        assert constraint.name == name
        assert constraint.violation_error_message == (violation_error_message or constraint.default_violation_error_message)

    if expected_error is RemovedInDjango60Warning:
        assert "Passing positional arguments to BaseConstraint is deprecated." in caplog.text