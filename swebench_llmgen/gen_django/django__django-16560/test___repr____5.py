import pytest
from django.contrib.auth.models import User
from django.db.models import CheckConstraint

@pytest.fixture
def check_constraint():
    return CheckConstraint(check=Q(id__gt=0), name='check_positive_id', violation_error_message='ID must be positive')

def test_repr_default(check_constraint):
    expected_repr = "<CheckConstraint: check=Q(id__gt=0) name='check_positive_id'>"
    assert repr(check_constraint) == expected_repr

def test_repr_with_violation_error_message(check_constraint):
    # Set a custom violation error message
    check_constraint.violation_error_message = 'Custom violation message'
    expected_repr = "<CheckConstraint: check=Q(id__gt=0) name='check_positive_id' violation_error_message='Custom violation message'>"
    assert repr(check_constraint) == expected_repr

def test_repr_without_violation_error_message(check_constraint):
    # Set the violation error message to None (simulate default case)
    check_constraint.violation_error_message = None
    expected_repr = "<CheckConstraint: check=Q(id__gt=0) name='check_positive_id'>"
    assert repr(check_constraint) == expected_repr