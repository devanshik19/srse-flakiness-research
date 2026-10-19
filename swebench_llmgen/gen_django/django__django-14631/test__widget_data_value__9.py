import pytest
from django.contrib.auth.models import User
from django.forms import TextInput
from django.utils.datastructures import MultiValueDict
from .forms import BaseForm

class TestBaseForm:
    
    @pytest.fixture
    def form_with_no_data(self):
        return BaseForm(data=MultiValueDict(), files=MultiValueDict())
    
    @pytest.fixture
    def form_with_data(self):
        data = MultiValueDict()
        data['username'] = 'testuser'
        files = MultiValueDict()
        return BaseForm(data=data, files=files)
    
    @pytest.fixture
    def text_input_widget(self):
        return TextInput()

    def test_widget_data_value_no_data(self, form_with_no_data, text_input_widget):
        html_name = 'username'
        assert form_with_no_data._widget_data_value(text_input_widget, html_name) is None

    def test_widget_data_value_with_data(self, form_with_data, text_input_widget):
        html_name = 'username'
        assert form_with_data._widget_data_value(text_input_widget, html_name) == 'testuser'