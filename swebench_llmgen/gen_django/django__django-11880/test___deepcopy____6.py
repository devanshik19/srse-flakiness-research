import pytest
from django.forms import Field
from django.contrib.auth.models import User
from django.forms.widgets import TextInput

@pytest.fixture
def field_instance():
    field = Field()
    field.widget = TextInput()
    field.validators = [lambda x: x]  # Simple validator for testing
    return field

def test_deepcopy(field_instance):
    copied_field = field_instance.__deepcopy__({})

    # Check that the copied field is a different instance
    assert copied_field is not field_instance

    # Check that the widget is deeply copied
    assert copied_field.widget is not field_instance.widget
    assert copied_field.widget.__class__ == field_instance.widget.__class__

    # Check that the validators are shallow copied
    assert copied_field.validators is not field_instance.validators
    assert copied_field.validators == field_instance.validators

    # Verify that the copied field maintains its original widget type
    assert isinstance(copied_field.widget, TextInput)
    
    # Ensure the original field's validators are unchanged
    assert field_instance.validators == [lambda x: x]