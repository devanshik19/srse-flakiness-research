import pytest
from django.forms.widgets import Widget
from django.contrib.auth.models import User

class BoundWidget:
    def __init__(self, parent_widget, data, renderer):
        self.parent_widget = parent_widget
        self.data = data

    def template_name(self):
        if 'template_name' in self.data:
            return self.data['template_name']
        return self.parent_widget.template_name


class TestBoundWidget:
    class MockWidget:
        template_name = 'default_template.html'

    def test_template_name_with_custom_template(self):
        parent_widget = self.MockWidget()
        data = {'template_name': 'custom_template.html'}
        widget = BoundWidget(parent_widget, data, None)

        assert widget.template_name() == 'custom_template.html'

    def test_template_name_without_custom_template(self):
        parent_widget = self.MockWidget()
        data = {}
        widget = BoundWidget(parent_widget, data, None)

        assert widget.template_name() == 'default_template.html'