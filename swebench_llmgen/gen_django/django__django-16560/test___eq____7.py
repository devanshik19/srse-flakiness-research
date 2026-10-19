import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import CheckConstraint

def test_check_constraint_eq():
    constraint1 = CheckConstraint(name='name1', check=Q(is_active=True), violation_error_message='Error 1')
    constraint2 = CheckConstraint(name='name1', check=Q(is_active=True), violation_error_message='Error 1')
    constraint3 = CheckConstraint(name='name2', check=Q(is_active=False), violation_error_message='Error 2')

    # Test equality with another instance of CheckConstraint
    assert constraint1 == constraint2

    # Test inequality with a different CheckConstraint
    assert constraint1 != constraint3

    # Test inequality with a non CheckConstraint object
    assert constraint1 != User(username='testuser')

    # Test equality with itself
    assert constraint1 == constraint1