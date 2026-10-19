import pytest
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class TestReadOnlyPasswordHashField:

    def test_init_with_default_params(self):
        field = ReadOnlyPasswordHashField()
        assert field.required is False

    def test_init_with_required_param(self):
        field = ReadOnlyPasswordHashField(required=True)
        assert field.required is True

    def test_init_with_custom_attributes(self):
        field = ReadOnlyPasswordHashField(label='Test Label', initial='default')
        assert field.label == 'Test Label'
        assert field.initial == 'default'
        assert field.required is False  # Default required should still be False