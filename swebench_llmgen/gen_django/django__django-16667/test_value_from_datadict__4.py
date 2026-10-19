import pytest
from django.contrib.auth.models import User
from django.forms.widgets import Widget

class TestWidget:
    @pytest.fixture
    def widget(self):
        return Widget()

    def test_value_from_datadict_with_value(self, widget):
        data = {'test_field': 'test_value'}
        files = {}
        name = 'test_field'
        result = widget.value_from_datadict(data, files, name)
        assert result == 'test_value'

    def test_value_from_datadict_with_none(self, widget):
        data = {}
        files = {}
        name = 'test_field'
        result = widget.value_from_datadict(data, files, name)
        assert result is None

    def test_value_from_datadict_with_different_name(self, widget):
        data = {'other_field': 'other_value'}
        files = {}
        name = 'test_field'
        result = widget.value_from_datadict(data, files, name)
        assert result is None