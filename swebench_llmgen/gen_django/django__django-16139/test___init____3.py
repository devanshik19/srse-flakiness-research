import pytest
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

@pytest.mark.django_db
def test_read_only_password_hash_field_init():
    # Test default initialization
    field = ReadOnlyPasswordHashField()
    assert field.required is False
    assert field.disabled is True

    # Test initialization with custom arguments
    field = ReadOnlyPasswordHashField(required=True, disabled=False)
    assert field.required is True
    assert field.disabled is False

    # Test initialization with only one custom argument
    field = ReadOnlyPasswordHashField(required=True)
    assert field.required is True
    assert field.disabled is True  # default should apply

    field = ReadOnlyPasswordHashField(disabled=False)
    assert field.required is False  # default should apply
    assert field.disabled is False

    # Test with no arguments passed
    field = ReadOnlyPasswordHashField()
    assert isinstance(field, forms.Field)  # It should be a Django form field