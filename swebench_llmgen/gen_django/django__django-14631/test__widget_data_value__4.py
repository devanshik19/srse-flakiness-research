import pytest
from django import forms
from django.forms import TextInput
from django.contrib.auth.models import User

class TestBaseForm(forms.BaseForm):

    def __init__(self, data=None, files=None, **kwargs):
        super().__init__(data=data, files=files, **kwargs)
        self.fields['username'] = forms.CharField(widget=TextInput())

@pytest.mark.parametrize(
    'data, expected_value',
    [
        ({'username': 'testuser'}, 'testuser'),  # valid input
        ({'username': ''}, ''),                    # empty input
        ({}, None)                                 # no input
    ]
)
def test_widget_data_value(data, expected_value):
    form = TestBaseForm(data=data)
    form.is_valid()
    widget = form.fields['username'].widget
    html_name = 'username'
    
    value = form._widget_data_value(widget, html_name)
    
    assert value == expected_value