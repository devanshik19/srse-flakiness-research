import pytest
from django.forms import Field
from django.contrib.auth.models import User
from django.forms.widgets import TextInput

def test_deepcopy_field():
    # Create an instance of the Field class
    original_field = Field(widget=TextInput(), validators=[])

    # Perform a deepcopy of the original field
    copied_field = original_field.__deepcopy__({})

    # Assertions to check if the copied field is a distinct object
    assert copied_field is not original_field  # copied_field should not be the same object
    assert copied_field.widget is not original_field.widget  # widget should be a new copy
    assert copied_field.validators == original_field.validators  # validators should be the same list
    assert copied_field.validators is not original_field.validators  # validators list should be a new copy