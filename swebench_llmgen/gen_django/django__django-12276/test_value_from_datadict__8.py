import pytest
from django.forms.widgets import Widget

class TestWidget:

    def test_value_from_datadict_with_value(self):
        widget = Widget()
        data = {'field_name': 'some_value'}
        files = {}
        name = 'field_name'
        result = widget.value_from_datadict(data, files, name)
        assert result == 'some_value'

    def test_value_from_datadict_without_value(self):
        widget = Widget()
        data = {'other_field_name': 'other_value'}
        files = {}
        name = 'field_name'
        result = widget.value_from_datadict(data, files, name)
        assert result is None

    def test_value_from_datadict_with_empty_string(self):
        widget = Widget()
        data = {'field_name': ''}
        files = {}
        name = 'field_name'
        result = widget.value_from_datadict(data, files, name)
        assert result == ''