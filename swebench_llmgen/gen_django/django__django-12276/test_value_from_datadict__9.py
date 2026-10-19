import pytest
from django.forms.widgets import Widget
from django.contrib.auth.models import User

class TestWidget:

    def test_value_from_datadict_with_value(self):
        widget = Widget()
        data = {'my_widget_name': 'test_value'}
        files = {}
        name = 'my_widget_name'
        
        result = widget.value_from_datadict(data, files, name)
        
        assert result == 'test_value'

    def test_value_from_datadict_without_value(self):
        widget = Widget()
        data = {}
        files = {}
        name = 'my_widget_name'
        
        result = widget.value_from_datadict(data, files, name)
        
        assert result is None

    def test_value_from_datadict_with_different_name(self):
        widget = Widget()
        data = {'other_widget_name': 'other_value'}
        files = {}
        name = 'my_widget_name'
        
        result = widget.value_from_datadict(data, files, name)
        
        assert result is None