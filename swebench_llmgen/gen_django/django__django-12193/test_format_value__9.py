import pytest
from django.forms.widgets import Widget
from django.utils import formats

class TestWidget:
    @pytest.fixture
    def widget(self):
        return Widget(attrs={})

    def test_format_value_empty_string(self, widget):
        assert widget.format_value('') is None

    def test_format_value_none(self, widget):
        assert widget.format_value(None) is None

    def test_format_value_non_localized(self, widget):
        widget.is_localized = False
        assert widget.format_value(123) == '123'
        assert widget.format_value('test') == 'test'

    def test_format_value_localized(self, widget, monkeypatch):
        widget.is_localized = True
        
        def mock_localize_input(value):
            return f"localized_{value}"

        monkeypatch.setattr(formats, 'localize_input', mock_localize_input)
        
        assert widget.format_value(123) == 'localized_123'
        assert widget.format_value('test') == 'localized_test'