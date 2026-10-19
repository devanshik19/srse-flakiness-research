import pytest
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

@pytest.mark.parametrize("required", [True, False])
def test_read_only_password_hash_field_init(required):
    # Create an instance of ReadOnlyPasswordHashField with different 'required' values
    field = ReadOnlyPasswordHashField(required=required)

    # Check if the 'required' property is set correctly
    assert field.required is False  # As per source code, default should override any value to False
    assert isinstance(field, forms.Field)  # Ensure it is an instance of forms.Field