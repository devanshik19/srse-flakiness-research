import pytest
from django.forms.widgets import Widget
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class MockParentWidget(Widget):
    template_name = 'default_template.html'

class BoundWidget:
    def __init__(self, parent_widget, data, renderer):
        self.parent_widget = parent_widget
        self.data = data
        self.renderer = renderer

    def template_name(self):
        if 'template_name' in self.data:
            return self.data['template_name']
        return self.parent_widget.template_name

def test_template_name_returns_custom_template_name():
    parent_widget = MockParentWidget()
    data = {'template_name': 'custom_template.html'}
    bound_widget = BoundWidget(parent_widget, data, None)
    
    assert bound_widget.template_name() == 'custom_template.html'

def test_template_name_returns_default_template_name():
    parent_widget = MockParentWidget()
    data = {}
    bound_widget = BoundWidget(parent_widget, data, None)
    
    assert bound_widget.template_name() == 'default_template.html'