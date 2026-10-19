import pytest
from django.forms.widgets import TextInput
from django.forms.boundfield import BoundWidget

@pytest.fixture
def bound_widget():
    parent_widget = TextInput()
    data_with_template = {'template_name': 'custom_template.html'}
    data_without_template = {}
    return {
        'widget_with_template': BoundWidget(parent_widget, data_with_template, None),
        'widget_without_template': BoundWidget(parent_widget, data_without_template, None)
    }

def test_template_name_with_custom_template(bound_widget):
    assert bound_widget['widget_with_template'].template_name() == 'custom_template.html'

def test_template_name_without_custom_template(bound_widget):
    assert bound_widget['widget_without_template'].template_name() == bound_widget['widget_without_template'].parent_widget.template_name