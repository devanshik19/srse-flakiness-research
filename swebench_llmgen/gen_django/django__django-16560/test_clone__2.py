import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):

    def __init__(self):
        self.default_violation_error_message = "Default error"
        self.violation_error_message = "Violation error"

    def deconstruct(self):
        return (self.__class__.__name__, self.default_violation_error_message, self.violation_error_message)

def test_clone_creates_identical_instance():
    original_constraint = TestBaseConstraint()
    cloned_constraint = original_constraint.clone()

    # Check if the clone is indeed a new instance
    assert cloned_constraint is not original_constraint

    # Check if the clone has the same attributes
    assert cloned_constraint.default_violation_error_message == original_constraint.default_violation_error_message
    assert cloned_constraint.violation_error_message == original_constraint.violation_error_message

def test_clone_preserves_class_type():
    original_constraint = TestBaseConstraint()
    cloned_constraint = original_constraint.clone()

    # Check if the class type of the clone is the same as the original
    assert isinstance(cloned_constraint, TestBaseConstraint)