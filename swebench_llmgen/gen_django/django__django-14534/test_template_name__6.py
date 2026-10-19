import pytest
from django.forms.widgets import TextInput
from django.contrib.auth.models import User

class BoundWidget:
    def __init__(self, parent_widget, data, renderer):
        self.parent_widget = parent_widget
        self.data = data
        self.renderer = renderer

    def template_name(self):
        if 'template_name' in self.data:
            return self.data['template_name']
        return self.parent_widget.template_name

def test_template_name_with_data():
    parent_widget = TextInput()
    data = {'template_name': 'custom_template.html'}
    widget = BoundWidget(parent_widget, data, None)
    
    assert widget.template_name() == 'custom_template.html'

def test_template_name_without_data():
    parent_widget = TextInput()
    data = {}
    widget = BoundWidget(parent_widget, data, None)
    
    assert widget.template_name() == parent_widget.template_name