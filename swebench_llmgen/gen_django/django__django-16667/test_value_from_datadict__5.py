import pytest
from django.contrib.auth.models import User
from django.forms.widgets import Widget

class TestWidget:
    def setup_method(self):
        self.widget = Widget(attrs={})

    def test_value_from_datadict_returns_value_when_key_exists(self):
        data = {'widget_name': 'test_value'}
        files = {}
        name = 'widget_name'
        result = self.widget.value_from_datadict(data, files, name)
        assert result == 'test_value'

    def test_value_from_datadict_returns_none_when_key_does_not_exist(self):
        data = {'other_name': 'test_value'}
        files = {}
        name = 'widget_name'
        result = self.widget.value_from_datadict(data, files, name)
        assert result is None

    def test_value_from_datadict_returns_none_with_empty_data(self):
        data = {}
        files = {}
        name = 'widget_name'
        result = self.widget.value_from_datadict(data, files, name)
        assert result is None