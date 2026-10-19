import pytest
from django.forms.fields import Field
from django.forms.widgets import TextInput

@pytest.fixture
def field_instance():
    return Field(widget=TextInput(), validators=[])

def test_deepcopy_field(field_instance):
    # Create a deepcopy
    copied_field = field_instance.__deepcopy__({})
    
    # Validate that the original and copied instances are different
    assert copied_field is not field_instance
    
    # Validate that the widget is deeply copied
    assert copied_field.widget is not field_instance.widget
    assert isinstance(copied_field.widget, TextInput)

    # Validate that validators are copied by reference
    assert copied_field.validators == field_instance.validators
    assert copied_field.validators is field_instance.validators