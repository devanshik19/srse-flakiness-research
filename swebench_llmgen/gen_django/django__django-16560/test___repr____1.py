import pytest
from django.contrib.auth.models import User
from django.db.models.constraints import CheckConstraint

def test_check_constraint_repr():
    # Create an instance of CheckConstraint
    constraint = CheckConstraint(
        check=Q(name__isnull=False), 
        name='check_name_not_null', 
        violation_error_message='Name cannot be null'
    )
    
    # Test the __repr__ method
    expected_repr = (
        "<CheckConstraint: check=Q(('name__isnull', False)) "
        "name='check_name_not_null' violation_error_message='Name cannot be null'>"
    )
    assert repr(constraint) == expected_repr

    # Test without a custom violation_error_message
    constraint_default_message = CheckConstraint(
        check=Q(name__isnull=False), 
        name='check_name_not_null'
    )
    expected_repr_default = (
        "<CheckConstraint: check=Q(('name__isnull', False)) "
        "name='check_name_not_null'>"
    )
    assert repr(constraint_default_message) == expected_repr_default