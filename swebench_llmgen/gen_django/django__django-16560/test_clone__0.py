import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):
    def __init__(self):
        super().__init__()
        self.default_violation_error_message = "Default error message"
        self.violation_error_message = "Violation error message"

    def deconstruct(self):
        return ("BaseConstraint", [], {"default_violation_error_message": self.default_violation_error_message, 
                                       "violation_error_message": self.violation_error_message})

def test_clone():
    original_constraint = TestBaseConstraint()
    cloned_constraint = original_constraint.clone()

    assert isinstance(cloned_constraint, TestBaseConstraint)
    assert cloned_constraint.default_violation_error_message == original_constraint.default_violation_error_message
    assert cloned_constraint.violation_error_message == original_constraint.violation_error_message
    assert cloned_constraint is not original_constraint  # Ensure it is a new instance