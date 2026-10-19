import pytest
from django.db.models.constraints import CheckConstraint

def test_check_constraint_eq():
    constraint1 = CheckConstraint(name='check1', check='field_name > 0', violation_error_message='Violation 1')
    constraint2 = CheckConstraint(name='check1', check='field_name > 0', violation_error_message='Violation 1')
    constraint3 = CheckConstraint(name='check2', check='field_name < 0', violation_error_message='Violation 2')

    # Test equal CheckConstraints
    assert constraint1 == constraint2

    # Test not equal CheckConstraint with different name
    assert constraint1 != constraint3

    # Test not equal CheckConstraint with different check
    constraint4 = CheckConstraint(name='check1', check='field_name < 0', violation_error_message='Violation 1')
    assert constraint1 != constraint4

    # Test not equal with non-CheckConstraint object
    assert constraint1 != 'some string'