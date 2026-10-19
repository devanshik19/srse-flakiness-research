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
    path, _, kwargs = constraint.deconstruct()
    
    assert path == "django.db.models.constraints.TestBaseConstraint"
    assert kwargs == {"name": "test_constraint"}

def test_deconstruct_with_custom_error_message():
    constraint = TestBaseConstraint(name="test_constraint", violation_error_message="Custom error message")
    path, _, kwargs = constraint.deconstruct()
    
    assert path == "django.db.models.constraints.TestBaseConstraint"
    assert kwargs == {
        "name": "test_constraint",
        "violation_error_message": "Custom error message"
    }

def test_deconstruct_with_none_error_message():
    constraint = TestBaseConstraint(name="test_constraint", violation_error_message=None)
    path, _, kwargs = constraint.deconstruct()
    
    assert path == "django.db.models.constraints.TestBaseConstraint"
    assert kwargs == {"name": "test_constraint"}