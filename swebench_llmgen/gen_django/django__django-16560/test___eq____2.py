import pytest
from django.db.models.constraints import CheckConstraint

def test_check_constraint_eq():
    constraint1 = CheckConstraint(name='constraint1', check=Q(age__gte=18), violation_error_message='Must be at least 18.')
    constraint2 = CheckConstraint(name='constraint1', check=Q(age__gte=18), violation_error_message='Must be at least 18.')
    constraint3 = CheckConstraint(name='constraint3', check=Q(age__gte=21), violation_error_message='Must be at least 21.')
    
    # Test equality with the same values
    assert constraint1 == constraint2
    
    # Test equality with different values
    assert constraint1 != constraint3
    
    # Test equality with a different type
    assert constraint1 != 'some string'
    
    # Test equality with None
    assert constraint1 != None