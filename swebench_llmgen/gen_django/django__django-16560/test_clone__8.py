import pytest
from django.contrib.auth.models import User
from django.db.models import Model
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):
    def __init__(self):
        super().__init__()
        self.default_violation_error_message = "Default message"
        self.violation_error_message = "Violation message"

    def deconstruct(self):
        return (self.__class__.__name__, [], {
            'default_violation_error_message': self.default_violation_error_message,
            'violation_error_message': self.violation_error_message
        })

def test_clone():
    constraint = TestBaseConstraint()
    
    # Ensure the original instance has the expected values
    assert constraint.default_violation_error_message == "Default message"
    assert constraint.violation_error_message == "Violation message"
    
    # Clone the instance
    cloned_constraint = constraint.clone()

    # Ensure the cloned instance is of the same class
    assert isinstance(cloned_constraint, TestBaseConstraint)
    
    # Ensure the cloned instance has the same attributes
    assert cloned_constraint.default_violation_error_message == "Default message"
    assert cloned_constraint.violation_error_message == "Violation message"

    # Ensure that cloning produces a different instance
    assert constraint is not cloned_constraint