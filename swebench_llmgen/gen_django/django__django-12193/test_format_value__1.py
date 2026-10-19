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

    def test_format_value_without_localization(self, widget):
        widget.is_localized = False
        value = 123
        assert widget.format_value(value) == str(value)

    def test_format_value_with_localization(self, widget, monkeypatch):
        widget.is_localized = True
        value = datetime.date(2021, 1, 1)
        
        # Mocking the formats.localize_input method
        original_localize_input = formats.localize_input
        monkeypatch.setattr(formats, 'localize_input', lambda v: f"Localized: {v}")

        try:
            assert widget.format_value(value) == "Localized: 2021-01-01"
        finally:
            monkeypatch.setattr(formats, 'localize_input', original_localize_input)