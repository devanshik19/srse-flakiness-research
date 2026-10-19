import pytest
from django.forms import widgets

class TestWidget:
    @pytest.fixture
    def widget(self):
        return widgets.Widget(attrs={})

    def test_format_value_empty_string(self, widget):
        assert widget.format_value('') is None

    def test_format_value_none(self, widget):
        assert widget.format_value(None) is None

    def test_format_value_non_localized(self, widget):
        widget.is_localized = False
        assert widget.format_value(123) == '123'
        assert widget.format_value(45.67) == '45.67'
        assert widget.format_value(datetime.datetime(2022, 1, 1, 12, 0)) == '2022-01-01 12:00:00'

    def test_format_value_localized(self, widget, monkeypatch):
        def mock_localize_input(value):
            return f"localized-{value}"

        widget.is_localized = True
        monkeypatch.setattr(widgets.formats, 'localize_input', mock_localize_input)

        assert widget.format_value(123) == 'localized-123'
        assert widget.format_value(45.67) == 'localized-45.67'
        assert widget.format_value(datetime.datetime(2022, 1, 1, 12, 0)) == 'localized-2022-01-01 12:00:00'