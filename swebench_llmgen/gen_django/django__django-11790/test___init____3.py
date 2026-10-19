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

    def test_init_with_default_kwargs(self):
        field = ReadOnlyPasswordHashField(label="Password", initial="test")
        assert field.label == "Password"
        assert field.initial == "test"
        assert field.required is False