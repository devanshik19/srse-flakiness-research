import pytest
from django.forms.widgets import Widget
from django.utils import formats

class TestWidget:

    @pytest.fixture
    def widget(self):
        return Widget(attrs={'class': 'test-widget'})

    def test_format_value_none(self, widget):
        assert widget.format_value(None) is None

    def test_format_value_empty_string(self, widget):
        assert widget.format_value('') is None

    def test_format_value_non_localized(self, widget):
        value = "test value"
        assert widget.format_value(value) == str(value)

    def test_format_value_localized(self, widget, monkeypatch):
        widget.is_localized = True
        
        # Simulate formats.localize_input
        def mock_localize_input(value):
            return f"localized: {value}"
        
        monkeypatch.setattr(formats, 'localize_input', mock_localize_input)

        value = "test value"
        assert widget.format_value(value) == "localized: test value"