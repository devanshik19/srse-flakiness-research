import pytest
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class TestReadOnlyPasswordHashField:

    def test_init_with_no_arguments(self):
        field = ReadOnlyPasswordHashField()
        assert field.required is False

    def test_init_with_required_false(self):
        field = ReadOnlyPasswordHashField(required=False)
        assert field.required is False

    def test_init_with_required_true(self):
        field = ReadOnlyPasswordHashField(required=True)
        assert field.required is True

    def test_init_with_custom_widget(self):
        widget = forms.TextInput()
        field = ReadOnlyPasswordHashField(widget=widget)
        assert field.widget == widget