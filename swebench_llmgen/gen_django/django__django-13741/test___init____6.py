import pytest
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class TestReadOnlyPasswordHashField:

    def test_init_with_required_false(self):
        field = ReadOnlyPasswordHashField()
        assert field.required is False

    def test_init_with_required_true(self):
        field = ReadOnlyPasswordHashField(required=True)
        assert field.required is True

    def test_init_with_custom_kwargs(self):
        field = ReadOnlyPasswordHashField(label='Custom Label', required=True)
        assert field.label == 'Custom Label'
        assert field.required is True

    def test_init_default_widget(self):
        field = ReadOnlyPasswordHashField()
        assert isinstance(field.widget, forms.Widget)

    def test_init_with_custom_widget(self):
        custom_widget = forms.TextInput()
        field = ReadOnlyPasswordHashField(widget=custom_widget)
        assert field.widget == custom_widget