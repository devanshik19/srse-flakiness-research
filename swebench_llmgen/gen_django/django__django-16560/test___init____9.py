import pytest
import warnings
from django.core.exceptions import ValidationError
from django.utils.deprecation import RemovedInDjango60Warning
from django.contrib.auth.models import User
from django.db.models import CharField
from django.db import models


class BaseConstraint:
    default_violation_error_message = "Default error message"

    def __init__(self, *args, name=None, violation_error_message=None):
        # RemovedInDjango60Warning.
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
        # RemovedInDjango60Warning.
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


def test_base_constraint_init_no_args():
    with pytest.raises(TypeError, match="missing 1 required keyword-only argument: 'name'"):
        BaseConstraint()


def test_base_constraint_init_with_name():
    constraint = BaseConstraint(name="unique_constraint")
    assert constraint.name == "unique_constraint"
    assert constraint.violation_error_message == constraint.default_violation_error_message


def test_base_constraint_init_with_violation_error_message():
    constraint = BaseConstraint(name="unique_constraint", violation_error_message="Custom error")
    assert constraint.violation_error_message == "Custom error"


def test_base_constraint_init_with_positional_args():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        constraint = BaseConstraint("unique_constraint", "Custom error")
        
        assert len(w) == 1
        assert issubclass(w[-1].category, RemovedInDjango60Warning)
        
        assert constraint.name == "unique_constraint"
        assert constraint.violation_error_message == "Custom error"


def test_base_constraint_init_with_only_two_positional_args():
    constraint = BaseConstraint("unique_constraint")
    assert constraint.name == "unique_constraint"
    assert constraint.violation_error_message == constraint.default_violation_error_message