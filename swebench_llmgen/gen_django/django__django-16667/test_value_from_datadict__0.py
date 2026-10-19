import pytest
from django.forms.widgets import Widget

class TestWidget:
    @pytest.fixture
    def widget(self):
        return Widget()

    def test_value_from_datadict_with_value(self, widget):
        data = {'test_name': 'test_value'}
        files = {}
        name = 'test_name'
        result = widget.value_from_datadict(data, files, name)
        assert result == 'test_value'
    
    def test_value_from_datadict_with_no_value(self, widget):
        data = {}
        files = {}
        name = 'test_name'
        result = widget.value_from_datadict(data, files, name)
        assert result is None

    def test_value_from_datadict_with_different_name(self, widget):
        data = {'other_name': 'other_value'}
        files = {}
        name = 'test_name'
        result = widget.value_from_datadict(data, files, name)
        assert result is None
        
    def test_value_from_datadict_with_empty_string(self, widget):
        data = {'test_name': ''}
        files = {}
        name = 'test_name'
        result = widget.value_from_datadict(data, files, name)
        assert result == ''