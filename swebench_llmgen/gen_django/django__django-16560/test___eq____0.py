import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import CheckConstraint

@pytest.mark.parametrize(
    "constraint1, constraint2, expected",
    [
        (
            CheckConstraint(name="check_name", check=Q(username__exact="test"), violation_error_message="error"),
            CheckConstraint(name="check_name", check=Q(username__exact="test"), violation_error_message="error"),
            True
        ),
        (
            CheckConstraint(name="check_name", check=Q(username__exact="test"), violation_error_message="error"),
            CheckConstraint(name="check_name", check=Q(username__exact="different"), violation_error_message="error"),
            False
        ),
        (
            CheckConstraint(name="check_name", check=Q(username__exact="test"), violation_error_message="error"),
            CheckConstraint(name="check_different", check=Q(username__exact="test"), violation_error_message="error"),
            False
        ),
        (
            CheckConstraint(name="check_name", check=Q(username__exact="test"), violation_error_message="error"),
            "string_representation",
            False
        ),
    ]
)
def test_check_constraint_equality(constraint1, constraint2, expected):
    assert (constraint1 == constraint2) == expected