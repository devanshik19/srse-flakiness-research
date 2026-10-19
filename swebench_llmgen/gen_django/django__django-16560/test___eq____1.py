import pytest
from django.db.models.constraints import CheckConstraint

@pytest.fixture
def check_constraint_1():
    return CheckConstraint(name='check_1', check='field > 0', violation_error_message='Must be greater than 0')

@pytest.fixture
def check_constraint_2():
    return CheckConstraint(name='check_1', check='field > 0', violation_error_message='Must be greater than 0')

@pytest.fixture
def check_constraint_3():
    return CheckConstraint(name='check_2', check='field <= 10', violation_error_message='Must be less than or equal to 10')

def test_eq_same_constraints(check_constraint_1, check_constraint_2):
    assert check_constraint_1 == check_constraint_2

def test_eq_different_name(check_constraint_1, check_constraint_3):
    assert check_constraint_1 != check_constraint_3

def test_eq_different_check_expression(check_constraint_1, check_constraint_3):
    assert check_constraint_1 != check_constraint_3

def test_eq_different_violation_error_message(check_constraint_1, check_constraint_3):
    assert check_constraint_1 != check_constraint_3

def test_eq_different_type(check_constraint_1):
    assert check_constraint_1 != "Not a CheckConstraint"