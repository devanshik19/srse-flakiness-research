import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class TestBaseForm(forms.BaseForm):
    class TestWidget:
        def value_from_datadict(self, data, files, html_name):
            return data.get(html_name, '')

    def setup_method(self):
        self.data = {'test_field': 'test_value'}
        self.files = {}
        self.form = TestBaseForm(self.data, self.files, None, '', None, None, '', None, None, None, None, None)

    def test_widget_data_value(self):
        widget = self.TestWidget()
        html_name = 'test_field'
        
        # Test retrieving data from widget
        result = self.form._widget_data_value(widget, html_name)
        assert result == 'test_value'
    
    def test_widget_data_value_no_data(self):
        widget = self.TestWidget()
        html_name = 'non_existent_field'
        
        # Test retrieving data when field does not exist
        result = self.form._widget_data_value(widget, html_name)
        assert result == ''