import pytest
from django.forms.widgets import Widget

class TestWidget:
    def test_value_from_datadict_returns_value_when_present(self):
        widget = Widget()
        data = {'field_name': 'test_value'}
        files = {}
        name = 'field_name'
        
        result = widget.value_from_datadict(data, files, name)
        
        assert result == 'test_value'

    def test_value_from_datadict_returns_none_when_not_present(self):
        widget = Widget()
        data = {'other_field': 'some_value'}
        files = {}
        name = 'field_name'
        
        result = widget.value_from_datadict(data, files, name)
        
        assert result is None

    def test_value_from_datadict_handles_empty_dict(self):
        widget = Widget()
        data = {}
        files = {}
        name = 'field_name'
        
        result = widget.value_from_datadict(data, files, name)
        
        assert result is None