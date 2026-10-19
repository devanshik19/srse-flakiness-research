import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):

    def __init__(self, name, violation_error_message=None):
        self.name = name
        self.violation_error_message = violation_error_message
        self.default_violation_error_message = "Default error message"

def test_deconstruct_with_default_error_message():
    constraint = TestBaseConstraint(name="test_constraint")
    expected_path = "django.db.models.constraints.TestBaseConstraint"
    expected_kwargs = {"name": "test_constraint"}
    
    assert constraint.deconstruct() == (expected_path.replace("django.db.models.constraints", "django.db.models"), (), expected_kwargs)

def test_deconstruct_with_custom_error_message():
    constraint = TestBaseConstraint(name="test_constraint", violation_error_message="Custom error message")
    expected_path = "django.db.models.constraints.TestBaseConstraint"
    expected_kwargs = {
        "name": "test_constraint",
        "violation_error_message": "Custom error message"
    }
    
    assert constraint.deconstruct() == (expected_path.replace("django.db.models.constraints", "django.db.models"), (), expected_kwargs)

def test_deconstruct_with_none_error_message():
    constraint = TestBaseConstraint(name="test_constraint", violation_error_message=None)
    expected_path = "django.db.models.constraints.TestBaseConstraint"
    expected_kwargs = {"name": "test_constraint"}

    assert constraint.deconstruct() == (expected_path.replace("django.db.models.constraints", "django.db.models"), (), expected_kwargs)