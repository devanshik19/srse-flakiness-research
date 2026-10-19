import pytest
from django.db.models.constraints import CheckConstraint

def test_check_constraint_eq_same_instance():
    constraint = CheckConstraint(name='my_constraint', check='column_name > 0', violation_error_message='Must be greater than zero')
    assert constraint == constraint

def test_check_constraint_eq_different_instance_same_values():
    constraint1 = CheckConstraint(name='my_constraint', check='column_name > 0', violation_error_message='Must be greater than zero')
    constraint2 = CheckConstraint(name='my_constraint', check='column_name > 0', violation_error_message='Must be greater than zero')
    assert constraint1 == constraint2

def test_check_constraint_eq_different_name():
    constraint1 = CheckConstraint(name='constraint_1', check='column_name > 0', violation_error_message='Must be greater than zero')
    constraint2 = CheckConstraint(name='constraint_2', check='column_name > 0', violation_error_message='Must be greater than zero')
    assert constraint1 != constraint2

def test_check_constraint_eq_different_check():
    constraint1 = CheckConstraint(name='my_constraint', check='column_name > 0', violation_error_message='Must be greater than zero')
    constraint2 = CheckConstraint(name='my_constraint', check='column_name < 0', violation_error_message='Must be greater than zero')
    assert constraint1 != constraint2

def test_check_constraint_eq_different_violation_error_message():
    constraint1 = CheckConstraint(name='my_constraint', check='column_name > 0', violation_error_message='Must be greater than zero')
    constraint2 = CheckConstraint(name='my_constraint', check='column_name > 0', violation_error_message='Must be a positive value')
    assert constraint1 != constraint2

def test_check_constraint_eq_different_type():
    constraint = CheckConstraint(name='my_constraint', check='column_name > 0', violation_error_message='Must be greater than zero')
    assert constraint != 'not_a_constraint'