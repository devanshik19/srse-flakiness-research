import pytest
from django.core.exceptions import ValidationError
from django.utils.deprecation import RemovedInDjango60Warning
from django.contrib.auth.models import User
from django.db import models


class BaseConstraint:
    default_violation_error_message = "Default violation error message."

    def __init__(self, *args, name=None, violation_error_message=None):
        if name is None and not args:
            raise TypeError(
                f"{self.__class__.__name__}.__init__() missing 1 required keyword-only "
                f"argument: 'name'"
            )
        self.name = name
        if violation_error_message is not None:
            self.violation_error_message = violation_error_message
        else:
            self.violation_error_message = self.default_violation_error_message
        if args:
            warnings.warn(
                f"Passing positional arguments to {self.__class__.__name__} is "
                f"deprecated.",
                RemovedInDjango60Warning,
                stacklevel=2,
            )
            for arg, attr in zip(args, ["name", "violation_error_message"]):
                if arg:
                    setattr(self, attr, arg)


def test_base_constraint_init_no_name():
    with pytest.raises(TypeError, match="missing 1 required keyword-only argument: 'name'"):
        BaseConstraint()


def test_base_constraint_init_with_name():
    constraint = BaseConstraint(name="unique_user_constraint")
    assert constraint.name == "unique_user_constraint"
    assert constraint.violation_error_message == constraint.default_violation_error_message


def test_base_constraint_init_with_violation_message():
    constraint = BaseConstraint(name="unique_user_constraint", violation_error_message="Custom error")
    assert constraint.violation_error_message == "Custom error"


def test_base_constraint_init_with_positional_args():
    with pytest.warns(RemovedInDjango60Warning):
        constraint = BaseConstraint("name_arg", "violation_arg")
    assert constraint.name == "name_arg"
    assert constraint.violation_error_message == "violation_arg"


def test_base_constraint_init_with_positional_arg_and_keyword_arg():
    with pytest.warns(RemovedInDjango60Warning):
        constraint = BaseConstraint("name_arg", violation_error_message="Custom error")
    assert constraint.name == "name_arg"
    assert constraint.violation_error_message == "Custom error"