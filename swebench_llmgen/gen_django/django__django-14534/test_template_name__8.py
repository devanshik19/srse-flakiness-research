import pytest
from django.forms.widgets import TextInput
from django.forms.boundfield import BoundWidget

class MockParentWidget:
    @property
    def template_name(self):
        return 'parent_template.html'

def test_template_name_with_data():
    data = {'template_name': 'custom_template.html'}
    parent_widget = MockParentWidget()
    bound_widget = BoundWidget(parent_widget, data, None)
    
    assert bound_widget.template_name() == 'custom_template.html'

def test_template_name_without_data():
    data = {}
    parent_widget = MockParentWidget()
    bound_widget = BoundWidget(parent_widget, data, None)
    
    assert bound_widget.template_name() == 'parent_template.html'