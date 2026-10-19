import pytest
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class TestReadOnlyPasswordHashField:

    def test_init_with_default_parameters(self):
        field = ReadOnlyPasswordHashField()
        assert field.required is False
        assert field.disabled is True

    def test_init_with_custom_parameters(self):
        field = ReadOnlyPasswordHashField(required=True, disabled=False)
        assert field.required is True
        assert field.disabled is False

    def test_init_with_only_required_parameter(self):
        field = ReadOnlyPasswordHashField(required=True)
        assert field.required is True
        assert field.disabled is True

    def test_init_with_only_disabled_parameter(self):
        field = ReadOnlyPasswordHashField(disabled=False)
        assert field.required is False
        assert field.disabled is False