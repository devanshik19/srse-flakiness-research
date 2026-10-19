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

    def test_format_value_string(self, widget):
        assert widget.format_value('test') == 'test'

    def test_format_value_integer(self, widget):
        assert widget.format_value(123) == '123'

    def test_format_value_float(self, widget):
        assert widget.format_value(123.45) == '123.45'
        
    def test_format_value_localized(self, widget, monkeypatch):
        widget.is_localized = True
        monkeypatch.setattr(formats, 'localize_input', lambda value: f"localized_{value}")
        assert widget.format_value(123.45) == 'localized_123.45'

    def test_format_value_localized_empty_string(self, widget, monkeypatch):
        widget.is_localized = True
        monkeypatch.setattr(formats, 'localize_input', lambda value: f"localized_{value}")
        assert widget.format_value('') is None

    def test_format_value_localized_none(self, widget, monkeypatch):
        widget.is_localized = True
        monkeypatch.setattr(formats, 'localize_input', lambda value: f"localized_{value}")
        assert widget.format_value(None) is None