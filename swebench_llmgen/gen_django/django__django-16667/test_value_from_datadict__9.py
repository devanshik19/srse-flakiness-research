import pytest
from django.contrib.auth.models import User
from django.forms.widgets import Widget

class TestWidget:

    def setup_method(self):
        self.widget = Widget()

    def test_value_from_datadict_returns_value_when_present(self):
        data = {'test_name': 'test_value'}
        files = {}
        name = 'test_name'
        result = self.widget.value_from_datadict(data, files, name)
        assert result == 'test_value'

    def test_value_from_datadict_returns_none_when_not_present(self):
        data = {'other_name': 'other_value'}
        files = {}
        name = 'test_name'
        result = self.widget.value_from_datadict(data, files, name)
        assert result is None

    def test_value_from_datadict_with_empty_data(self):
        data = {}
        files = {}
        name = 'test_name'
        result = self.widget.value_from_datadict(data, files, name)
        assert result is None