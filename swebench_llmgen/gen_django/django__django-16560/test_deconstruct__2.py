import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):
    default_violation_error_message = "Default error message"
    violation_error_message = None

    def __init__(self, name):
        self.name = name

def test_deconstruct_default_violation_message():
    constraint = TestBaseConstraint(name='test_constraint')
    result = constraint.deconstruct()
    assert result == (
        'django.db.models.constraints.TestBaseConstraint',
        (),
        {'name': 'test_constraint'}
    )

def test_deconstruct_custom_violation_message():
    constraint = TestBaseConstraint(name='test_constraint')
    constraint.violation_error_message = "Custom error message"
    result = constraint.deconstruct()
    assert result == (
        'django.db.models.constraints.TestBaseConstraint',
        (),
        {'name': 'test_constraint', 'violation_error_message': 'Custom error message'}
    )

def test_deconstruct_violation_message_none():
    constraint = TestBaseConstraint(name='test_constraint')
    constraint.violation_error_message = None
    result = constraint.deconstruct()
    assert result == (
        'django.db.models.constraints.TestBaseConstraint',
        (),
        {'name': 'test_constraint'}
    )