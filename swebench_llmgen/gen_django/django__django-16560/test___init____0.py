import pytest
import warnings
from django.core.exceptions import ValidationError
from django.utils.deprecation import RemovedInDjango60Warning
from django.contrib.auth.models import User
from django.db.models import BaseConstraint

def test_base_constraint_init_no_name_or_args():
    with pytest.raises(TypeError, match="missing 1 required keyword-only argument: 'name'"):
        BaseConstraint()  # No arguments provided

def test_base_constraint_init_with_name():
    constraint = BaseConstraint(name='unique_constraint')
    assert constraint.name == 'unique_constraint'
    assert constraint.violation_error_message == constraint.default_violation_error_message

def test_base_constraint_init_with_violation_error_message():
    constraint = BaseConstraint(name='unique_constraint', violation_error_message='Custom error message')
    assert constraint.violation_error_message == 'Custom error message'

def test_base_constraint_init_with_positional_args():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        constraint = BaseConstraint('positional_name', 'Custom error message')
        assert len(w) == 1
        assert issubclass(w[-1].category, RemovedInDjango60Warning)
        assert constraint.name == 'positional_name'
        assert constraint.violation_error_message == 'Custom error message'