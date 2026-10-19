import pytest
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

def test_read_only_password_hash_field_init_default_values():
    field = ReadOnlyPasswordHashField()

    # Check default values
    assert field.required is False
    assert field.disabled is True

def test_read_only_password_hash_field_init_custom_values():
    field = ReadOnlyPasswordHashField(required=True, disabled=False)

    # Check overridden values
    assert field.required is True
    assert field.disabled is False

def test_read_only_password_hash_field_init_no_overrides():
    field = ReadOnlyPasswordHashField()

    # Check that the base class __init__ is called properly
    assert field.widget is not None
    assert isinstance(field.widget, forms.Widget)