import pytest
from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import ReadOnlyPasswordHashField

class TestReadOnlyPasswordHashField:
    def test_init_with_required_set_to_false(self):
        field = ReadOnlyPasswordHashField(required=False)
        assert not field.required

    def test_init_with_required_set_to_true(self):
        field = ReadOnlyPasswordHashField(required=True)
        assert field.required

    def test_init_without_required_setting(self):
        field = ReadOnlyPasswordHashField()
        assert not field.required

    def test_init_with_additional_args(self):
        field = ReadOnlyPasswordHashField(label="Test Label", initial="initial_value")
        assert field.label == "Test Label"
        assert field.initial == "initial_value"