import pytest
from django.forms.widgets import Widget
from django.utils import formats

class TestWidget:

    def test_format_value_empty_string(self):
        widget = Widget()
        result = widget.format_value('')
        assert result is None

    def test_format_value_none(self):
        widget = Widget()
        result = widget.format_value(None)
        assert result is None

    def test_format_value_localized(self, monkeypatch):
        widget = Widget()
        widget.is_localized = True

        # Simulate the localize_input method for the test
        def mock_localize_input(value):
            return f"localized-{value}"

        monkeypatch.setattr(formats, 'localize_input', mock_localize_input)
        result = widget.format_value('test')
        assert result == 'localized-test'

    def test_format_value_non_localized(self):
        widget = Widget()
        widget.is_localized = False
        result = widget.format_value('test')
        assert result == 'test'

    def test_format_value_integer(self):
        widget = Widget()
        result = widget.format_value(123)
        assert result == '123'

    def test_format_value_float(self):
        widget = Widget()
        result = widget.format_value(123.45)
        assert result == '123.45'