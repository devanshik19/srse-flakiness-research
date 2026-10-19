import pytest
from django import forms
from django.contrib.auth.models import User
from django.exceptions import ValidationError

from django.contrib.auth.forms import ReadOnlyPasswordHashField

def test_readonly_password_hash_field_init():
    # Test default initialization (required=False)
    field = ReadOnlyPasswordHashField()
    assert not field.required

    # Test initialization with required=True
    field_required = ReadOnlyPasswordHashField(required=True)
    assert field_required.required

    # Test initialization with required=False explicitly set
    field_explicit = ReadOnlyPasswordHashField(required=False)
    assert not field_explicit.required

    # Test initialization with other arguments
    field_with_widget = ReadOnlyPasswordHashField(widget=forms.TextInput())
    assert isinstance(field_with_widget.widget, forms.TextInput)