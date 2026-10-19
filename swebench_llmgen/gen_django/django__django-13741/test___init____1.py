import pytest
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class TestReadOnlyPasswordHashField:
    
    def test_init_with_default_required(self):
        field = ReadOnlyPasswordHashField()
        assert not field.required

    def test_init_with_required_true(self):
        field = ReadOnlyPasswordHashField(required=True)
        assert field.required

    def test_init_with_required_false(self):
        field = ReadOnlyPasswordHashField(required=False)
        assert not field.required

    def test_init_with_additional_kwargs(self):
        field = ReadOnlyPasswordHashField(label="Test Label", initial="test_initial")
        assert field.label == "Test Label"
        assert field.initial == "test_initial"
        assert not field.required