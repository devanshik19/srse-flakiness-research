import pytest
from django.forms import BaseForm, widgets
from django.contrib.auth.models import User

class TestBaseForm(BaseForm):
    def __init__(self, data=None, files=None):
        super().__init__(data=data, files=files, auto_id="id_%s", prefix=None, 
                         initial=None, error_class=None, label_suffix=None, 
                         empty_permitted=None, field_order=None, 
                         use_required_attribute=None, renderer=None)

def test_widget_data_value_with_valid_data():
    data = {'my_widget': 'test_value'}
    files = {}
    form = TestBaseForm(data=data, files=files)
    widget = widgets.TextInput()
    value = form._widget_data_value(widget, 'my_widget')
    assert value == 'test_value'

def test_widget_data_value_with_missing_data():
    data = {}
    files = {}
    form = TestBaseForm(data=data, files=files)
    widget = widgets.TextInput()
    value = form._widget_data_value(widget, 'my_widget')
    assert value is None

def test_widget_data_value_with_file_field():
    data = {'my_file': 'test_file'}
    files = {'my_file': 'test_file_content'}
    form = TestBaseForm(data=data, files=files)
    widget = widgets.FileInput()
    value = form._widget_data_value(widget, 'my_file')
    assert value == 'test_file_content'