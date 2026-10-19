import pytest
from django.forms.widgets import Widget


class TestWidget:
    def setup_method(self):
        self.widget = Widget()

    def test_value_from_datadict_returns_value(self):
        data = {'widget_name': 'test_value'}
        files = {}
        name = 'widget_name'
        result = self.widget.value_from_datadict(data, files, name)
        assert result == 'test_value'

    def test_value_from_datadict_returns_none_if_not_provided(self):
        data = {}
        files = {}
        name = 'widget_name'
        result = self.widget.value_from_datadict(data, files, name)
        assert result is None

    def test_value_from_datadict_with_empty_string(self):
        data = {'widget_name': ''}
        files = {}
        name = 'widget_name'
        result = self.widget.value_from_datadict(data, files, name)
        assert result == ''

    def test_value_from_datadict_with_missing_name(self):
        data = {'other_widget': 'value'}
        files = {}
        name = 'widget_name'
        result = self.widget.value_from_datadict(data, files, name)
        assert result is None