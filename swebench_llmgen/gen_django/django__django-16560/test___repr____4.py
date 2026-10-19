import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import CheckConstraint

def test_check_constraint_repr():
    # Create a CheckConstraint instance
    check_constraint = CheckConstraint(
        check=Q(username__isnull=False),
        name='username_not_null',
        violation_error_message='Username cannot be null.'
    )
    
    # Expected repr output
    expected_repr = (
        "<CheckConstraint: check=Q(username__isnull=False) "
        "name='username_not_null' violation_error_message='Username cannot be null.'>"
    )

    assert repr(check_constraint) == expected_repr
    
    # Test without a custom violation error message
    check_constraint_default_message = CheckConstraint(
        check=Q(email__isnull=False),
        name='email_not_null'
    )
    
    expected_repr_default = (
        "<CheckConstraint: check=Q(email__isnull=False) "
        "name='email_not_null'>"
    )
    
    assert repr(check_constraint_default_message) == expected_repr_default