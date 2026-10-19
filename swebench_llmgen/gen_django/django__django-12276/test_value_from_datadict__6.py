import pytest
from django.forms.widgets import Widget

class TestWidget:
    def test_value_from_datadict_with_valid_data(self):
        widget = Widget()
        data = {'name': 'test_value'}
        files = {}
        name = 'name'
        result = widget.value_from_datadict(data, files, name)
        assert result == 'test_value'

    def test_value_from_datadict_with_missing_data(self):
        widget = Widget()
        data = {}
        files = {}
        name = 'name'
        result = widget.value_from_datadict(data, files, name)
        assert result is None

    def test_value_from_datadict_with_empty_string(self):
        widget = Widget()
        data = {'name': ''}
        files = {}
        name = 'name'
        result = widget.value_from_datadict(data, files, name)
        assert result == ''