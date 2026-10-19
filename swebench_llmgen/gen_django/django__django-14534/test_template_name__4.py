import pytest
from django.forms.widgets import TextInput
from django.forms import BoundField

class BoundWidget:
    def __init__(self, parent_widget, data, renderer):
        self.parent_widget = parent_widget
        self.data = data
        self.renderer = renderer

    def template_name(self):
        if 'template_name' in self.data:
            return self.data['template_name']
        return self.parent_widget.template_name

@pytest.fixture
def setup_bound_widget():
    parent_widget = TextInput()  # Using TextInput as the parent widget
    return BoundWidget(parent_widget, {}, None)

def test_template_name_default(setup_bound_widget):
    bound_widget = setup_bound_widget
    expected_template_name = bound_widget.parent_widget.template_name
    assert bound_widget.template_name() == expected_template_name

def test_template_name_custom(setup_bound_widget):
    bound_widget = setup_bound_widget
    bound_widget.data = {'template_name': 'custom_template.html'}
    assert bound_widget.template_name() == 'custom_template.html'