import pytest
from django.forms.widgets import Widget
from django.utils import formats

class MockWidget(Widget):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.is_localized = False

def test_format_value_none():
    widget = MockWidget()
    assert widget.format_value(None) is None

def test_format_value_empty_string():
    widget = MockWidget()
    assert widget.format_value('') is None

def test_format_value_str():
    widget = MockWidget()
    assert widget.format_value('test') == 'test'

def test_format_value_integer():
    widget = MockWidget()
    assert widget.format_value(123) == '123'

def test_format_value_float():
    widget = MockWidget()
    assert widget.format_value(123.45) == '123.45'

def test_format_value_localized():
    widget = MockWidget()
    widget.is_localized = True
    value = datetime.datetime(2023, 1, 1, 12, 0, 0)
    localized_value = formats.localize_input(value)
    assert widget.format_value(value) == localized_value