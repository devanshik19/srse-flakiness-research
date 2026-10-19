import pytest
from django.forms.widgets import Widget
from django.utils import formats

class TestWidget:

    def setup_method(self):
        self.widget = Widget(attrs={})
        self.widget.is_localized = False  # Test case when not localized

    def test_format_value_empty_string(self):
        assert self.widget.format_value('') is None

    def test_format_value_none(self):
        assert self.widget.format_value(None) is None

    def test_format_value_non_localized(self):
        value = 123
        assert self.widget.format_value(value) == str(value)

    def test_format_value_localized(self):
        self.widget.is_localized = True
        value = 123.456
        expected_value = formats.localize_input(value)
        assert self.widget.format_value(value) == expected_value