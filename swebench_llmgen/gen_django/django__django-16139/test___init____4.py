import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ReadOnlyPasswordHashField(forms.Field):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        kwargs.setdefault("disabled", True)
        super().__init__(*args, **kwargs)


def test_read_only_password_hash_field_init():
    # Test with default parameters
    field = ReadOnlyPasswordHashField()
    assert not field.required
    assert field.disabled

    # Test with custom parameters
    field = ReadOnlyPasswordHashField(required=True, disabled=False)
    assert field.required
    assert not field.disabled

    # Test with both parameters set to default values through kwargs
    field = ReadOnlyPasswordHashField(required=False, disabled=True)
    assert not field.required
    assert field.disabled

    # Test with disabling required and custom initialization
    field = ReadOnlyPasswordHashField(disabled=True)
    assert not field.required
    assert field.disabled