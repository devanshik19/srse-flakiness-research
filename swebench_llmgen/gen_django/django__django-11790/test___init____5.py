import pytest
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class TestReadOnlyPasswordHashField:

    def test_init_with_default_required(self):
        field = ReadOnlyPasswordHashField()
        assert not field.required  # Default should be False

    def test_init_with_required_true(self):
        field = ReadOnlyPasswordHashField(required=True)
        assert field.required  # Should be True when set

    def test_init_with_custom_args(self):
        field = ReadOnlyPasswordHashField(label="Custom Label", initial="initial_value")
        assert field.label == "Custom Label"
        assert field.initial == "initial_value"
        assert not field.required  # Still default to False