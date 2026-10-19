import pytest
from django.forms import BaseForm, CharField, TextInput
from django.contrib.auth.models import User

class TestBaseForm(BaseForm):
    field = CharField(widget=TextInput)

@pytest.fixture
def example_form():
    data = {'field': 'example data'}
    files = {}
    return TestBaseForm(data=data, files=files, auto_id='id_%s', 
                         prefix='', initial=None, 
                         error_class=None, label_suffix='', 
                         empty_permitted=True, 
                         field_order=None, use_required_attribute=True, 
                         renderer=None)

def test_widget_data_value(example_form):
    widget = example_form.fields['field'].widget
    html_name = 'field'
    
    # Call the method
    value = example_form._widget_data_value(widget, html_name)
    
    # Check the output
    assert value == 'example data'

def test_widget_data_value_with_empty_data(example_form):
    empty_form = TestBaseForm(data={}, files={}, auto_id='id_%s', 
                               prefix='', initial=None, 
                               error_class=None, label_suffix='', 
                               empty_permitted=True, 
                               field_order=None, use_required_attribute=True, 
                               renderer=None)
    widget = empty_form.fields['field'].widget
    html_name = 'field'
    
    # Call the method with empty data
    value = empty_form._widget_data_value(widget, html_name)
    
    # Check the output
    assert value == ''