import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):
    def deconstruct(self):
        return (self.__class__.__name__, self.fields, {})

def test_clone_creates_new_instance():
    # Arrange
    original_constraint = TestBaseConstraint()
    
    # Act
    cloned_constraint = original_constraint.clone()
    
    # Assert
    assert isinstance(cloned_constraint, TestBaseConstraint)
    assert cloned_constraint.fields == original_constraint.fields
    assert cloned_constraint is not original_constraint
    assert cloned_constraint.__class__ is original_constraint.__class__

def test_clone_with_different_fields():
    # Arrange
    class CustomConstraint(TestBaseConstraint):
        def __init__(self, fields):
            self.fields = fields
    
    original_constraint = CustomConstraint(fields=['field1', 'field2'])
    
    # Act
    cloned_constraint = original_constraint.clone()
    
    # Assert
    assert cloned_constraint.fields == original_constraint.fields