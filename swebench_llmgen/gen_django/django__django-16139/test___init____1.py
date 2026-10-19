import pytest
from django import forms
from django.contrib.auth.models import User

class ReadOnlyPasswordHashField(forms.Field):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        kwargs.setdefault("disabled", True)
        super().__init__(*args, **kwargs)

def test_read_only_password_hash_field_init():
    # Test default initialization
    field = ReadOnlyPasswordHashField()
    assert not field.required  # Default should be False
    assert field.disabled  # Default should be True

    # Test custom initialization
    field = ReadOnlyPasswordHashField(required=True, disabled=False)
    assert field.required  # Should be True
    assert not field.disabled  # Should be False

    # Test initialization with only required set
    field = ReadOnlyPasswordHashField(required=True)
    assert field.required  # Should be True
    assert field.disabled  # Should still be True by default

    # Test initialization with only disabled set
    field = ReadOnlyPasswordHashField(disabled=False)
    assert not field.required  # Should still be False by default
    assert not field.disabled  # Should be False