import pytest
from django.forms import BoundWidget
from django.forms.widgets import TextInput

@pytest.fixture
def setup_widget():
    parent_widget = TextInput()
    data = {'template_name': 'custom_template.html'}
    return BoundWidget(parent_widget=parent_widget, data=data, renderer=None)

def test_template_name_with_custom_template(setup_widget):
    widget = setup_widget
    assert widget.template_name() == 'custom_template.html'

def test_template_name_with_default_template():
    parent_widget = TextInput()
    data = {}
    widget = BoundWidget(parent_widget=parent_widget, data=data, renderer=None)
    assert widget.template_name() == parent_widget.template_name