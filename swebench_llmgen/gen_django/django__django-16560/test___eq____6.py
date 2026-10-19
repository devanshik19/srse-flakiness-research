import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import CheckConstraint

def test_check_constraint_eq():
    check_constraint_1 = CheckConstraint(name='check_1', check=Q(username__exact='test_user'), violation_error_message='Test error message')
    check_constraint_2 = CheckConstraint(name='check_1', check=Q(username__exact='test_user'), violation_error_message='Test error message')
    check_constraint_3 = CheckConstraint(name='check_2', check=Q(username__exact='another_user'), violation_error_message='Another error message')

    # Test equality with identical CheckConstraints
    assert check_constraint_1 == check_constraint_2

    # Test inequality with different CheckConstraints
    assert check_constraint_1 != check_constraint_3

    # Test inequality with a different type
    assert check_constraint_1 != 'not a CheckConstraint'