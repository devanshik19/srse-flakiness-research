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

    def test_format_value_localized(self, widget):
        widget.is_localized = True
        value = datetime.datetime(2023, 1, 1, 12, 0)
        expected_output = formats.localize_input(value)
        assert widget.format_value(value) == expected_output

    def test_format_value_non_localized(self, widget):
        widget.is_localized = False
        value = 12345
        assert widget.format_value(value) == str(value)

    def test_format_value_string(self, widget):
        widget.is_localized = False
        value = "test"
        assert widget.format_value(value) == "test"