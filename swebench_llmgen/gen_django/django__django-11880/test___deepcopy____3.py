import pytest
from django.forms import fields
from django.contrib.auth.models import User

def test_deepcopy():
    # Create an instance of Field
    field = fields.Field()
    field.widget = fields.TextInput()
    field.validators = [fields.validators.MaxLengthValidator(10)]

    # Perform a deepcopy
    copied_field = field.__deepcopy__({})

    # Assert that the copied object is a different instance
    assert copied_field is not field
    # Assert that the widget is a deep copy
    assert copied_field.widget is not field.widget
    # Assert that the validators list is a shallow copy
    assert copied_field.validators is not field.validators
    assert copied_field.validators[0] is field.validators[0]

    # Check the state of the original and copied field
    assert copied_field.widget.__class__ == field.widget.__class__
    assert copied_field.validators == field.validators