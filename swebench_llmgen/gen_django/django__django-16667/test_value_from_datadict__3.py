import pytest
from django.contrib.auth.models import User
from django.forms.widgets import Widget

class TestWidget:
    
    @pytest.fixture
    def widget(self):
        return Widget()

    def test_value_from_datadict returns_value(self, widget):
        data = {'name': 'test_value'}
        files = {}
        name = 'name'
        assert widget.value_from_datadict(data, files, name) == 'test_value'

    def test_value_from_datadict_returns_none_if_not_provided(self, widget):
        data = {}
        files = {}
        name = 'name'
        assert widget.value_from_datadict(data, files, name) is None

    def test_value_from_datadict_none_value(self, widget):
        data = {'name': None}
        files = {}
        name = 'name'
        assert widget.value_from_datadict(data, files, name) is None