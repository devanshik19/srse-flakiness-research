import pytest
from django.forms.widgets import TextInput
from django.forms.boundfield import BoundWidget

@pytest.mark.parametrize("data, expected_template_name", [
    ({"template_name": "custom_template.html"}, "custom_template.html"),
    ({}, "default_template.html")  # Assume 'default_template.html' as the fallback template
])
def test_template_name(data, expected_template_name):
    parent_widget = TextInput(template_name="default_template.html")
    bound_widget = BoundWidget(parent_widget, data, None)

    assert bound_widget.template_name() == expected_template_name