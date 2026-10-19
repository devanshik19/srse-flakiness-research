import pytest
from django.contrib.auth.models import User
from django.db.models import CheckConstraint


def test_check_constraint_repr():
    # Test default representation
    check_constraint = CheckConstraint(
        check=Q(username__isnull=False), 
        name='username_check'
    )
    expected_repr = "<CheckConstraint: check=Q(username__isnull=False) name='username_check'>"
    assert repr(check_constraint) == expected_repr

    # Test representation with a custom violation error message
    check_constraint.violation_error_message = "Custom violation message"
    expected_repr_with_error_message = "<CheckConstraint: check=Q(username__isnull=False) name='username_check' violation_error_message='Custom violation message'>"
    assert repr(check_constraint) == expected_repr_with_error_message

    # Test representation with default violation error message
    check_constraint.violation_error_message = check_constraint.default_violation_error_message
    expected_repr_default_error_message = "<CheckConstraint: check=Q(username__isnull=False) name='username_check'>"
    assert repr(check_constraint) == expected_repr_default_error_message