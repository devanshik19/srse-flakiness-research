import pytest
from django.contrib.auth.forms import ReadOnlyPasswordHashField

def test_read_only_password_hash_field_init_with_default_args():
    field = ReadOnlyPasswordHashField()
    assert field.required is False

def test_read_only_password_hash_field_init_with_required_true():
    field = ReadOnlyPasswordHashField(required=True)
    assert field.required is True

def test_read_only_password_hash_field_init_with_initial_kwargs():
    field = ReadOnlyPasswordHashField(label='Test Label', initial='initial_value')
    assert field.label == 'Test Label'
    assert field.initial == 'initial_value'

def test_read_only_password_hash_field_init_with_custom_widget():
    from django.forms import TextInput
    field = ReadOnlyPasswordHashField(widget=TextInput(attrs={'class': 'custom-class'}))
    assert isinstance(field.widget, TextInput)
    assert field.widget.attrs['class'] == 'custom-class'