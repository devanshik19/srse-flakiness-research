import pytest
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class TestReadOnlyPasswordHashField:

    def test_init_without_required(self):
        """Test ReadOnlyPasswordHashField initialized without required."""
        field = ReadOnlyPasswordHashField()
        assert field.required is False

    def test_init_with_required(self):
        """Test ReadOnlyPasswordHashField initialized with required=True."""
        field = ReadOnlyPasswordHashField(required=True)
        assert field.required is True

    def test_init_with_other_kwargs(self):
        """Test ReadOnlyPasswordHashField initialized with other kwargs."""
        field = ReadOnlyPasswordHashField(label="Test Label", help_text="Test help text")
        assert field.label == "Test Label"
        assert field.help_text == "Test help text"