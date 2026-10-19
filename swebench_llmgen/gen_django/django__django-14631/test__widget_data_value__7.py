import pytest
from django.forms import BaseForm, Field
from django.forms.widgets import TextInput
from django.utils.datastructures import MultiValueDict

class TestWidgetDataValue:
    
    class TestForm(BaseForm):
        field = Field(widget=TextInput)

    def test_widget_data_value(self):
        # Setup data and files for the form instance
        data = MultiValueDict({'field': 'test_value'})
        files = MultiValueDict()
        form = self.TestForm(data=data, files=files, auto_id='id_%s', prefix='', 
                             initial={}, error_class=None, label_suffix='', 
                             empty_permitted=False, field_order=None, 
                             use_required_attribute=True, renderer=None)
        
        # Prepare the widget instance
        widget = form.fields['field'].widget
        html_name = 'field'
        
        # Call the method being tested
        value = form._widget_data_value(widget, html_name)
        
        # Assert the expected value is returned
        assert value == 'test_value'

    def test_widget_data_value_with_no_data(self):
        # Setup form with empty data
        data = MultiValueDict()
        files = MultiValueDict()
        form = self.TestForm(data=data, files=files, auto_id='id_%s', prefix='', 
                             initial={}, error_class=None, label_suffix='', 
                             empty_permitted=False, field_order=None, 
                             use_required_attribute=True, renderer=None)
        
        # Prepare the widget instance
        widget = form.fields['field'].widget
        html_name = 'field'
        
        # Call the method being tested
        value = form._widget_data_value(widget, html_name)
        
        # Assert the expected value is `None` or default behavior
        assert value is None