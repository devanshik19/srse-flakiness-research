import pytest
from django import forms
from django.forms.widgets import TextInput
from django.http import QueryDict

class TestBaseForm(forms.BaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TestWidgetDataValue:

    @pytest.fixture
    def setup_form(self):
        data = QueryDict('username=johndoe')
        files = QueryDict('')
        form = TestBaseForm(data=data, files=files)
        return form

    @pytest.fixture
    def text_input_widget(self):
        return TextInput()

    def test_widget_data_value_valid(self, setup_form, text_input_widget):
        value = setup_form._widget_data_value(text_input_widget, 'username')
        assert value == 'johndoe'

    def test_widget_data_value_empty(self, setup_form, text_input_widget):
        setup_form.data = QueryDict('')
        value = setup_form._widget_data_value(text_input_widget, 'username')
        assert value == ''

    def test_widget_data_value_invalid_field(self, setup_form, text_input_widget):
        value = setup_form._widget_data_value(text_input_widget, 'non_existent_field')
        assert value is None