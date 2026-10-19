import pytest
from django.contrib.auth.models import User
from django.db.models import CheckConstraint

def test_check_constraint_repr():
    # Create an instance of CheckConstraint
    check_constraint = CheckConstraint(
        check=Q(username__isnull=False),
        name='username_not_null',
        violation_error_message='Username cannot be null'
    )

    # Expected representation string
    expected_repr = (
        "<CheckConstraint: check=Q(username__isnull=False) name='username_not_null' "
        "violation_error_message='Username cannot be null'>"
    )

    # Assert that the repr matches the expected string
    assert repr(check_constraint) == expected_repr

    # Create another instance of CheckConstraint with default violation error message
    check_constraint_default_msg = CheckConstraint(
        check=Q(email__isnull=False),
        name='email_not_null',
        violation_error_message=None
    )

    # Expected representation string without custom violation error message
    expected_repr_default_msg = (
        "<CheckConstraint: check=Q(email__isnull=False) name='email_not_null'>"
    )

    # Assert that the repr matches the expected string
    assert repr(check_constraint_default_msg) == expected_repr_default_msg