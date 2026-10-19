import pytest
from django.contrib.auth.models import User
from django.db.models import CheckConstraint

def test_check_constraint_eq():
    constraint1 = CheckConstraint(name='constraint1', check=Q(username__isnull=False), violation_error_message='Username cannot be null')
    constraint2 = CheckConstraint(name='constraint1', check=Q(username__isnull=False), violation_error_message='Username cannot be null')
    constraint3 = CheckConstraint(name='constraint3', check=Q(username__isnull=True), violation_error_message='Username can be null')

    # Test equality with the same attributes
    assert constraint1 == constraint2

    # Test inequality with different attributes
    assert constraint1 != constraint3

    # Test inequality with a different type
    assert constraint1 != 'not_a_constraint'