import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import BaseConstraint


class TestBaseConstraint(BaseConstraint):
    def __init__(self, name, violation_error_message=None):
        self.name = name
        self.default_violation_error_message = "Default error message"
        self.violation_error_message = violation_error_message


def test_deconstruct_with_default_message():
    constraint = TestBaseConstraint(name="test_constraint")
    path, _, kwargs = constraint.deconstruct()
    assert path == "django.db.models.TestBaseConstraint"
    assert kwargs == {"name": "test_constraint"}


def test_deconstruct_with_custom_message():
    custom_message = "Custom error message"
    constraint = TestBaseConstraint(name="test_constraint", violation_error_message=custom_message)
    path, _, kwargs = constraint.deconstruct()
    assert path == "django.db.models.TestBaseConstraint"
    assert kwargs == {
        "name": "test_constraint",
        "violation_error_message": custom_message,
    }


def test_deconstruct_without_violation_message():
    constraint = TestBaseConstraint(name="test_constraint", violation_error_message=None)
    path, _, kwargs = constraint.deconstruct()
    assert path == "django.db.models.TestBaseConstraint"
    assert kwargs == {"name": "test_constraint"}