import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):
    def deconstruct(self):
        return 'test_constraint', 'test', [], {}

def test_clone():
    constraint = TestBaseConstraint()
    cloned_constraint = constraint.clone()

    assert isinstance(cloned_constraint, TestBaseConstraint)
    assert cloned_constraint.deconstruct() == constraint.deconstruct()
    assert cloned_constraint is not constraint