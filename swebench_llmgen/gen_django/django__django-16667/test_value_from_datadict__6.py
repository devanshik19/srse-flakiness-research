import pytest
from django.contrib.auth.models import User
from django.forms.widgets import Widget

class TestWidget:
    
    @pytest.fixture
    def widget(self):
        return Widget()

    def test_value_from_datadict_returns_value(self, widget):
        data = {'test_name': 'test_value'}
        files = {}
        name = 'test_name'
        result = widget.value_from_datadict(data, files, name)
        assert result == 'test_value'

    def test_value_from_datadict_returns_none_if_key_not_present(self, widget):
        data = {'other_name': 'other_value'}
        files = {}
        name = 'test_name'
        result = widget.value_from_datadict(data, files, name)
        assert result is None

    def test_value_from_datadict_returns_none_with_empty_data(self, widget):
        data = {}
        files = {}
        name = 'test_name'
        result = widget.value_from_datadict(data, files, name)
        assert result is None