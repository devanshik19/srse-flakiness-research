import pytest
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

def test_read_only_password_hash_field_init():
    # Test with default arguments
    field = ReadOnlyPasswordHashField()
    assert field.required is False
    assert field.disabled is True

    # Test with explicit arguments
    field = ReadOnlyPasswordHashField(required=True, disabled=False)
    assert field.required is True
    assert field.disabled is False

    # Test with other field attributes
    field = ReadOnlyPasswordHashField(label="Password")
    assert field.label == "Password"

    # Test if the field is an instance of forms.Field
    assert isinstance(field, forms.Field)