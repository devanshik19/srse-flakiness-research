import pytest
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

def test_readonly_password_hash_field_init():
    # Test with no args
    field = ReadOnlyPasswordHashField()
    assert field.required is False
    assert field.disabled is True

    # Test with custom arguments
    field = ReadOnlyPasswordHashField(required=True, disabled=False)
    assert field.required is True
    assert field.disabled is False

    # Test with custom args and kwargs: should keep `disabled=True` and `required=False` as defaults
    field = ReadOnlyPasswordHashField(required=False, disabled=True)
    assert field.required is False
    assert field.disabled is True