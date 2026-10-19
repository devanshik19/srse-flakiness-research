import pytest
from django.forms import BoundWidget
from django.forms.widgets import TextInput


class MockParentWidget:
    template_name = 'default_template.html'


@pytest.fixture
def bound_widget_with_data():
    data = {'template_name': 'custom_template.html'}
    parent_widget = MockParentWidget()
    return BoundWidget(parent_widget=parent_widget, data=data, renderer=None)


@pytest.fixture
def bound_widget_without_data():
    data = {}
    parent_widget = MockParentWidget()
    return BoundWidget(parent_widget=parent_widget, data=data, renderer=None)


def test_template_name_with_data(bound_widget_with_data):
    assert bound_widget_with_data.template_name() == 'custom_template.html'


def test_template_name_without_data(bound_widget_without_data):
    assert bound_widget_without_data.template_name() == 'default_template.html'