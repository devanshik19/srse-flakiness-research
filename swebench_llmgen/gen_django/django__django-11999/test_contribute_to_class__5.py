import pytest
from django.contrib.auth.models import User
from django.db.models import Field


class CustomField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attname = "custom_field"
        self.column = "custom_field"
        self.name = "custom_field"
        self.choices = None


def test_contribute_to_class():
    # Arrange
    custom_field = CustomField()

    # Act
    custom_field.contribute_to_class(User, 'custom_field')

    # Assert
    assert hasattr(User, 'custom_field')
    assert isinstance(getattr(User, 'custom_field'), CustomField)
    assert User._meta.get_field('custom_field') == custom_field
    
    # Assert descriptor class handling
    assert hasattr(User, 'get_custom_field_display') is False

    # Act - setting up a new field with a different name
    custom_field_2 = CustomField()
    custom_field_2.attname = "another_field"
    custom_field_2.column = "another_field"
    custom_field_2.name = "another_field"

    custom_field_2.contribute_to_class(User, 'another_field')
    
    # Assert that we have both fields set up correctly
    assert hasattr(User, 'another_field')
    assert isinstance(getattr(User, 'another_field'), CustomField)
    assert User._meta.get_field('another_field') == custom_field_2

    # Assert that each field can be accessed as attributes in User
    assert User.custom_field != User.another_field