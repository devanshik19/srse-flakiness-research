import pytest
from django.contrib.auth.models import User
from django.forms.widgets import Widget

class TestWidget:

    def test_value_from_datadict_with_existing_key(self):
        widget = Widget()
        data = {'name': 'test_value'}
        files = {}
        name = 'name'
        result = widget.value_from_datadict(data, files, name)
        assert result == 'test_value'

    def test_value_from_datadict_with_nonexistent_key(self):
        widget = Widget()
        data = {'other_name': 'test_value'}
        files = {}
        name = 'name'
        result = widget.value_from_datadict(data, files, name)
        assert result is None

    def test_value_from_datadict_with_empty_data(self):
        widget = Widget()
        data = {}
        files = {}
        name = 'name'
        result = widget.value_from_datadict(data, files, name)
        assert result is None

    def test_value_from_datadict_with_non_string_data(self):
        widget = Widget()
        data = {'name': None}
        files = {}
        name = 'name'
        result = widget.value_from_datadict(data, files, name)
        assert result is None