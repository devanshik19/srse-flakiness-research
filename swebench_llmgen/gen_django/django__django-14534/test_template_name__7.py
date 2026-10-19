import pytest
from django.forms import BoundWidget
from django.contrib.auth.models import User

class MockParentWidget:
    @property
    def template_name(self):
        return 'default_template.html'

@pytest.mark.parametrize("data, expected_template", [
    ({'template_name': 'custom_template.html'}, 'custom_template.html'),
    ({}, 'default_template.html'),
])
def test_template_name(data, expected_template):
    parent_widget = MockParentWidget()
    widget = BoundWidget(parent_widget=parent_widget, data=data, renderer=None)
    
    assert widget.template_name() == expected_template