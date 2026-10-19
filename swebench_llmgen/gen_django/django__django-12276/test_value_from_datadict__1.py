import pytest
from django.forms.widgets import Widget

class TestWidget:
    def test_value_from_datadict_exists(self):
        widget = Widget()
        data = {'test_name': 'test_value'}
        files = {}
        name = 'test_name'
        
        result = widget.value_from_datadict(data, files, name)
        
        assert result == 'test_value'

    def test_value_from_datadict_not_found(self):
        widget = Widget()
        data = {}
        files = {}
        name = 'non_existent_name'
        
        result = widget.value_from_datadict(data, files, name)
        
        assert result is None

    def test_value_from_datadict_empty_data(self):
        widget = Widget()
        data = {}
        files = {}
        name = 'empty_name'
        
        result = widget.value_from_datadict(data, files, name)
        
        assert result is None

    def test_value_from_datadict_with_files(self):
        widget = Widget()
        data = {'file_name': 'file_value'}
        files = {}
        name = 'file_name'
        
        result = widget.value_from_datadict(data, files, name)
        
        assert result == 'file_value'