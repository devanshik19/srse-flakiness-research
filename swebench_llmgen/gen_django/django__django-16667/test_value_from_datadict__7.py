import pytest
from django.forms.widgets import Widget
from django.contrib.auth.models import User

class TestWidget:

    def test_value_from_datadict_with_value(self):
        widget = Widget()
        data = {'test_name': 'test_value'}
        files = {}
        name = 'test_name'
        result = widget.value_from_datadict(data, files, name)
        assert result == 'test_value'

    def test_value_from_datadict_with_nonexistent_key(self):
        widget = Widget()
        data = {'another_name': 'another_value'}
        files = {}
        name = 'test_name'
        result = widget.value_from_datadict(data, files, name)
        assert result is None

    def test_value_from_datadict_empty_data(self):
        widget = Widget()
        data = {}
        files = {}
        name = 'test_name'
        result = widget.value_from_datadict(data, files, name)
        assert result is None