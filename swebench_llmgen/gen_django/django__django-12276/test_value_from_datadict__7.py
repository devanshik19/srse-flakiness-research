import pytest
from django.forms.widgets import Widget

class TestWidget:
    
    def test_value_from_datadict_key_exists(self):
        widget = Widget()
        data = {'name': 'test_value'}
        files = {}
        name = 'name'
        
        result = widget.value_from_datadict(data, files, name)
        
        assert result == 'test_value'
        
    def test_value_from_datadict_key_not_exists(self):
        widget = Widget()
        data = {}
        files = {}
        name = 'name'
        
        result = widget.value_from_datadict(data, files, name)
        
        assert result is None
        
    def test_value_from_datadict_empty_data(self):
        widget = Widget()
        data = {}
        files = {}
        name = 'non_existent_key'
        
        result = widget.value_from_datadict(data, files, name)
        
        assert result is None
        
    def test_value_from_datadict_with_files(self):
        widget = Widget()
        data = {'name': 'test_value'}
        files = {'name': 'file_value'}
        name = 'name'
        
        result = widget.value_from_datadict(data, files, name)
        
        assert result == 'test_value'