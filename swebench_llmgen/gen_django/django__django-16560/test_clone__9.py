import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):
    def __init__(self):
        self.default_violation_error_message = "Default error"
        self.violation_error_message = "Violation error"

    def deconstruct(self):
        return ('app_label', 'constraint_name', [self.default_violation_error_message], {})

def test_clone_method():
    constraint = TestBaseConstraint()
    
    # Clone the constraint
    cloned_constraint = constraint.clone()
    
    # Assert that the cloned constraint is an instance of the same class
    assert isinstance(cloned_constraint, TestBaseConstraint)
    
    # Assert that the cloned constraint is a different instance
    assert cloned_constraint is not constraint
    
    # Assert that attributes are the same
    assert cloned_constraint.default_violation_error_message == constraint.default_violation_error_message
    assert cloned_constraint.violation_error_message == constraint.violation_error_message