import pytest
import warnings
from django.core.exceptions import ValidationError
from django.utils.deprecation import RemovedInDjango60Warning
from django.contrib.auth.models import User
from django.db.models import BaseConstraint

def test_base_constraint_init_no_args():
    with pytest.raises(TypeError, match="missing 1 required keyword-only argument: 'name'"):
        BaseConstraint()

def test_base_constraint_init_with_name():
    constraint = BaseConstraint(name='test_constraint')
    assert constraint.name == 'test_constraint'
    assert constraint.violation_error_message == constraint.default_violation_error_message

def test_base_constraint_init_with_violation_error_message():
    constraint = BaseConstraint(name='test_constraint', violation_error_message='Test violation')
    assert constraint.violation_error_message == 'Test violation'

def test_base_constraint_init_with_positionals():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        constraint = BaseConstraint('test_constraint', 'Test violation')
        assert len(w) == 1
        assert issubclass(w[-1].category, RemovedInDjango60Warning)
        assert constraint.name == 'test_constraint'
        assert constraint.violation_error_message == 'Test violation'