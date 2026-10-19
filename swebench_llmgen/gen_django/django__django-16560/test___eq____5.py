import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import CheckConstraint

def test_check_constraint_eq():
    constraint1 = CheckConstraint(
        name='constraint1',
        check=Exists(User.objects.filter(username=F('username'))),
        violation_error_message='Error Message 1'
    )
    constraint2 = CheckConstraint(
        name='constraint1',
        check=Exists(User.objects.filter(username=F('username'))),
        violation_error_message='Error Message 1'
    )
    constraint3 = CheckConstraint(
        name='constraint2',
        check=Exists(User.objects.filter(username=F('username'))),
        violation_error_message='Error Message 2'
    )
    
    # Test equality with identical CheckConstraint instances
    assert constraint1 == constraint2
    
    # Test inequality with different CheckConstraint instances
    assert constraint1 != constraint3
    
    # Test equality with a different type
    assert constraint1 != 'not_a_constraint'