import pytest
import warnings
from django.db.models import BaseConstraint
from django.utils.deprecation import RemovedInDjango60Warning
from django.core.exceptions import ValidationError

def test_base_constraint_init_without_name():
    with pytest.raises(TypeError, match="missing 1 required keyword-only argument: 'name'"):
        BaseConstraint()

def test_base_constraint_init_with_name():
    constraint = BaseConstraint(name='test_constraint')
    assert constraint.name == 'test_constraint'
    assert constraint.violation_error_message == constraint.default_violation_error_message

def test_base_constraint_init_with_violation_error_message():
    constraint = BaseConstraint(name='test_constraint', violation_error_message='Custom error message')
    assert constraint.violation_error_message == 'Custom error message'

def test_base_constraint_init_with_positional_arguments():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        constraint = BaseConstraint('test_constraint', 'Custom error message')
        assert len(w) == 1
        assert issubclass(w[-1].category, RemovedInDjango60Warning)
    assert constraint.name == 'test_constraint'
    assert constraint.violation_error_message == 'Custom error message'