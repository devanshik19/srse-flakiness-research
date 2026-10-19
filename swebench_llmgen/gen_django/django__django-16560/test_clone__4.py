import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):
    def __init__(self):
        super().__init__()
        self.default_violation_error_message = "Default violation error"
        self.violation_error_message = "Violation error"

    def deconstruct(self):
        return ('app_label', 'model_name', 'field_name', 
                {'default_violation_error_message': self.default_violation_error_message,
                 'violation_error_message': self.violation_error_message})

def test_clone():
    constraint = TestBaseConstraint()
    cloned_constraint = constraint.clone()
    
    assert isinstance(cloned_constraint, TestBaseConstraint)
    assert cloned_constraint.default_violation_error_message == constraint.default_violation_error_message
    assert cloned_constraint.violation_error_message == constraint.violation_error_message
    assert cloned_constraint is not constraint  # Ensure it's a different instance