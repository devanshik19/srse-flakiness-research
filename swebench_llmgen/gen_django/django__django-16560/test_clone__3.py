import pytest
from django.contrib.auth.models import User
from django.db.models import Constraints
from django.core.exceptions import ValidationError

class BaseConstraint:
    def __init__(self):
        self.default_violation_error_message = "Default violation"
        self.violation_error_message = "Violation occurred"

    def deconstruct(self):
        return (self.__class__.__name__, [], {})
    
    def clone(self):
        _, args, kwargs = self.deconstruct()
        return self.__class__(*args, **kwargs)

def test_clone():
    # Create an instance of the BaseConstraint class
    original_constraint = BaseConstraint()

    # Clone the original constraint
    cloned_constraint = original_constraint.clone()

    # Assert that the original and cloned instances are not the same object
    assert original_constraint is not cloned_constraint
    
    # Assert that they are of the same class
    assert isinstance(cloned_constraint, BaseConstraint)
    
    # Assert that the fields are the same
    assert original_constraint.default_violation_error_message == cloned_constraint.default_violation_error_message
    assert original_constraint.violation_error_message == cloned_constraint.violation_error_message