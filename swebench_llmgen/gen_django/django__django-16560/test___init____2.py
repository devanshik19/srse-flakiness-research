import pytest
import warnings
from django.core.exceptions import ValidationError
from django.utils.deprecation import RemovedInDjango60Warning
from django.contrib.auth.models import User
from django.db.models.constraints import BaseConstraint

def test_base_constraint_init_no_name():
    with pytest.raises(TypeError, match="missing 1 required keyword-only argument: 'name'"):
        BaseConstraint()

def test_base_constraint_init_with_name():
    constraint = BaseConstraint(name='unique_constraint')
    assert constraint.name == 'unique_constraint'
    assert constraint.violation_error_message == constraint.default_violation_error_message

def test_base_constraint_init_with_violation_error_message():
    constraint = BaseConstraint(name='unique_constraint', violation_error_message='Violation!')
    assert constraint.violation_error_message == 'Violation!'

def test_base_constraint_init_with_positional_args():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        constraint = BaseConstraint('unique_constraint', 'Violation!')
        assert len(w) == 1
        assert issubclass(w[-1].category, RemovedInDjango60Warning)
        assert constraint.name == 'unique_constraint'
        assert constraint.violation_error_message == 'Violation!'

def test_base_constraint_init_violation_error_message_default():
    constraint = BaseConstraint(name='unique_constraint')
    expected_message = constraint.default_violation_error_message
    assert constraint.violation_error_message == expected_message