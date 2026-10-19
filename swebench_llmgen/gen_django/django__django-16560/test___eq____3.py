import pytest
from django.db.models.constraints import CheckConstraint

def test_check_constraint_eq():
    # Create two identical CheckConstraint instances
    constraint1 = CheckConstraint(name='constraint1', check=Q(id__gt=0), violation_error_message='Invalid ID')
    constraint2 = CheckConstraint(name='constraint1', check=Q(id__gt=0), violation_error_message='Invalid ID')
    
    assert constraint1 == constraint2  # They should be equal
    
    # Create a different CheckConstraint instance
    constraint3 = CheckConstraint(name='constraint2', check=Q(id__gte=0), violation_error_message='Invalid ID')
    
    assert constraint1 != constraint3  # They should not be equal
    assert constraint2 != constraint3  # They should not be equal

    # Compare with a different type
    assert constraint1 != 'some_string'  # Check against a non-CheckConstraint
    
    # Check against None
    assert constraint1 != None  # Check against None

    # Test with a new instance with same properties but different reference
    constraint4 = CheckConstraint(name='constraint1', check=Q(id__gt=0), violation_error_message='Different Message')
    
    assert constraint1 != constraint4  # They should not be equal due to different error messages