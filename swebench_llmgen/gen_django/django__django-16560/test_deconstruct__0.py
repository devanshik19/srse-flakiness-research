import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):
    def __init__(self, name, violation_error_message=None):
        self.name = name
        self.violation_error_message = violation_error_message
        self.default_violation_error_message = "Default error"

def test_deconstruct_with_default_message():
    constraint = TestBaseConstraint(name='my_constraint')
    expected = (
        'django.db.models.constraints.TestBaseConstraint',
        (),
        {'name': 'my_constraint'}
    )
    assert constraint.deconstruct() == expected

def test_deconstruct_with_custom_message():
    constraint = TestBaseConstraint(name='my_constraint', violation_error_message='This is a custom error')
    expected = (
        'django.db.models.constraints.TestBaseConstraint',
        (),
        {'name': 'my_constraint', 'violation_error_message': 'This is a custom error'}
    )
    assert constraint.deconstruct() == expected

def test_deconstruct_with_default_violation_error_message():
    constraint = TestBaseConstraint(name='my_constraint', violation_error_message='Default error')
    expected = (
        'django.db.models.constraints.TestBaseConstraint',
        (),
        {'name': 'my_constraint'}
    )
    assert constraint.deconstruct() == expected