import pytest
from django.forms import fields
from django.contrib.auth.models import User

def test_field_deepcopy():
    # Create an instance of the Field class
    field_instance = fields.Field()
    field_instance.widget = fields.TextInput()
    field_instance.validators = [lambda x: None]  # Simple no-op validator

    # Perform deepcopy operation
    deep_copied_instance = field_instance.__deepcopy__({})

    # Assert that the deep copied instance is not the same object
    assert deep_copied_instance is not field_instance

    # Assert that the widget is a deep copy
    assert deep_copied_instance.widget is not field_instance.widget
    assert isinstance(deep_copied_instance.widget, fields.TextInput)

    # Assert that validators list is a new copy
    assert deep_copied_instance.validators is not field_instance.validators
    assert deep_copied_instance.validators == field_instance.validators

    # Assert that the original instance remains unchanged
    assert field_instance.validators == [lambda x: None]
    field_instance.validators.append(lambda x: x)  # Modify original instance
    assert deep_copied_instance.validators == [lambda x: None]  # Should remain unchanged