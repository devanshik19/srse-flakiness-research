import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ReadOnlyPasswordHashField(forms.Field):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    def bound_data(self, data, initial):
        return data

    def has_changed(self, initial, data):
        return initial != data


def test_read_only_password_hash_field_init():
    # Test without 'required' in kwargs
    field = ReadOnlyPasswordHashField()
    assert field.required is False
    
    # Test with 'required' set to True
    field = ReadOnlyPasswordHashField(required=True)
    assert field.required is True

    # Test with 'required' set to False
    field = ReadOnlyPasswordHashField(required=False)
    assert field.required is False

    # Test with extra args
    field = ReadOnlyPasswordHashField(label='Test Label', initial='Test Initial')
    assert field.label == 'Test Label'
    assert field.initial == 'Test Initial'
    assert field.required is False  # should still default to False

    # Test with an unexpected keyword argument (ValidationError should not be raised)
    with pytest.raises(TypeError):
        ReadOnlyPasswordHashField(unexpected_arg=True)

    # Test if the widget is correctly set to default
    assert isinstance(field.widget, forms.Widget)