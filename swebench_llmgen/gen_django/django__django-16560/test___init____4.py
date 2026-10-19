import pytest
import warnings
from django.core.exceptions import ValidationError
from django.utils.deprecation import RemovedInDjango60Warning
from django.contrib.auth.models import User
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint:

    def test_init_without_name_and_args_raises_type_error(self):
        with pytest.raises(TypeError, match="missing 1 required keyword-only argument: 'name'"):
            BaseConstraint()

    def test_init_with_name(self):
        constraint = BaseConstraint(name="my_constraint")
        assert constraint.name == "my_constraint"
        assert constraint.violation_error_message == constraint.default_violation_error_message

    def test_init_with_violation_error_message(self):
        error_message = "This is a custom violation error message."
        constraint = BaseConstraint(name="my_constraint", violation_error_message=error_message)
        assert constraint.violation_error_message == error_message

    def test_init_with_positional_args(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            constraint = BaseConstraint("my_constraint", "This is a custom violation error message.")
            assert len(w) == 1
            assert issubclass(w[-1].category, RemovedInDjango60Warning)
            assert constraint.name == "my_constraint"
            assert constraint.violation_error_message == "This is a custom violation error message."