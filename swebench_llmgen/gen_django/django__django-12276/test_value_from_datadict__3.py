import pytest
from django.forms.widgets import Widget

class TestWidget:
    @pytest.fixture
    def widget(self):
        return Widget()

    def test_value_from_datadict_existing_key(self, widget):
        data = {'test_key': 'test_value'}
        files = {}
        name = 'test_key'
        result = widget.value_from_datadict(data, files, name)
        assert result == 'test_value'

    def test_value_from_datadict_non_existing_key(self, widget):
        data = {'another_key': 'another_value'}
        files = {}
        name = 'test_key'
        result = widget.value_from_datadict(data, files, name)
        assert result is None

    def test_value_from_datadict_empty_data(self, widget):
        data = {}
        files = {}
        name = 'test_key'
        result = widget.value_from_datadict(data, files, name)
        assert result is None

    def test_value_from_datadict_with_empty_string(self, widget):
        data = {'test_key': ''}
        files = {}
        name = 'test_key'
        result = widget.value_from_datadict(data, files, name)
        assert result == ''