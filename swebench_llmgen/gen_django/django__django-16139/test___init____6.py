import pytest
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

def test_readonly_password_hash_field_init():
    # Test default initialization
    field = ReadOnlyPasswordHashField()
    assert field.required is False
    assert field.disabled is True
    
    # Test initialization with custom arguments
    field = ReadOnlyPasswordHashField(required=True, disabled=False)
    assert field.required is True
    assert field.disabled is False
    
    # Test initialization without 'required' argument
    field = ReadOnlyPasswordHashField(disabled=False)
    assert field.required is False
    assert field.disabled is False
    
    # Test initialization without 'disabled' argument
    field = ReadOnlyPasswordHashField(required=True)
    assert field.required is True
    assert field.disabled is True