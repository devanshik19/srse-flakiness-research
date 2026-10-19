import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):
    def deconstruct(self):
        # Assuming this is how the deconstruct method behaves for the test
        return (self.__class__.__name__, [], {})

def test_clone():
    constraint = TestBaseConstraint()
    
    cloned_constraint = constraint.clone()
    
    assert isinstance(cloned_constraint, TestBaseConstraint)
    assert cloned_constraint.deconstruct() == constraint.deconstruct()