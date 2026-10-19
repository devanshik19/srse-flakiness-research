import pytest
from django.forms.fields import Field
from django.forms.widgets import TextInput

@pytest.mark.parametrize("widget_type", [TextInput,])
def test_deepcopy_field(widget_type):
    # Create an instance of the Field class with a widget
    original_field = Field()
    original_field.widget = widget_type()
    original_field.validators = [lambda x: x]  # Example validator

    # Perform the deepcopy
    copied_field = original_field.__deepcopy__({})

    # Assertions to validate deepcopy
    assert copied_field is not original_field  # Ensure it's a new instance
    assert copied_field.widget is not original_field.widget  # Widget should be a new instance
    assert copied_field.validators == original_field.validators  # Validators should be the same
    assert copied_field.widget == original_field.widget  # Widget content should be the same