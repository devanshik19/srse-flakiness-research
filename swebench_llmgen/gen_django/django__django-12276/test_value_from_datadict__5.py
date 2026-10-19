import pytest
from django.forms.widgets import Widget

class TestWidget:
    def test_value_from_datadict(self):
        widget = Widget()
        
        # Test with existing key
        data = {'name': 'value'}
        files = {}
        name = 'name'
        result = widget.value_from_datadict(data, files, name)
        assert result == 'value'

        # Test with non-existing key
        name = 'non_existent_name'
        result = widget.value_from_datadict(data, files, name)
        assert result is None

        # Test with empty data
        data = {}
        result = widget.value_from_datadict(data, files, name)
        assert result is None
        
        # Test with None input for data
        result = widget.value_from_datadict(None, files, name)
        assert result is None