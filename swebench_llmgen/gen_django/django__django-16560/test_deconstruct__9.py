import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):
    def __init__(self, name, violation_error_message=None):
        self.name = name
        self.violation_error_message = violation_error_message
        self.default_violation_error_message = "Default error"

def test_deconstruct_without_custom_error_message():
    constraint = TestBaseConstraint(name="unique_email")
    path, _, kwargs = constraint.deconstruct()
    
    assert path == "django.db.models.TestBaseConstraint"
    assert kwargs == {"name": "unique_email"}

def test_deconstruct_with_custom_error_message():
    constraint = TestBaseConstraint(name="unique_email", violation_error_message="Custom error message")
    path, _, kwargs = constraint.deconstruct()
    
    assert path == "django.db.models.TestBaseConstraint"
    assert kwargs == {
        "name": "unique_email",
        "violation_error_message": "Custom error message"
    }

def test_deconstruct_with_default_message():
    constraint = TestBaseConstraint(name="unique_email", violation_error_message="Default error")
    path, _, kwargs = constraint.deconstruct()
    
    assert path == "django.db.models.TestBaseConstraint"
    assert kwargs == {"name": "unique_email"}