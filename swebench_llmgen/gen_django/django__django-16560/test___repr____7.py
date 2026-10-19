import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import CheckConstraint

def test_check_constraint_repr():
    # Create a CheckConstraint instance with some dummy parameters
    check_constraint = CheckConstraint(
        name="my_check_constraint",
        check=Q(username__isnull=False),  # Example condition
        violation_error_message="Username cannot be null"
    )
    
    # Expected representation string
    expected_repr = "<CheckConstraint: check=Q(username__isnull=False) name='my_check_constraint' violation_error_message='Username cannot be null'>"
    assert repr(check_constraint) == expected_repr

    # Create another CheckConstraint with default violation_error_message
    check_constraint_default = CheckConstraint(
        name="default_violation_check_constraint",
        check=Q(is_active=True)  # Example condition
    )
    
    # Expected representation string without custom violation_error_message
    expected_repr_default = "<CheckConstraint: check=Q(is_active=True) name='default_violation_check_constraint'>"
    assert repr(check_constraint_default) == expected_repr_default