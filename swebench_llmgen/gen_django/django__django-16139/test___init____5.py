import pytest
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

def test_readonly_password_hash_field_initialization():
    # Test default initialization
    field = ReadOnlyPasswordHashField()
    assert field.required is False
    assert field.disabled is True
    
    # Test custom initialization with required=True
    field_with_required = ReadOnlyPasswordHashField(required=True)
    assert field_with_required.required is True
    assert field_with_required.disabled is True  # should remain disabled
    
    # Test custom initialization with disabled=False
    field_with_disabled = ReadOnlyPasswordHashField(disabled=False)
    assert field_with_disabled.required is False  # should remain not required
    assert field_with_disabled.disabled is False
    
    # Test custom initialization with both required and disabled
    field_custom = ReadOnlyPasswordHashField(required=True, disabled=False)
    assert field_custom.required is True
    assert field_custom.disabled is False