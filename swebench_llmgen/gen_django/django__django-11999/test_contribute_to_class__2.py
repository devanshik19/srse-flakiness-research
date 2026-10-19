import pytest
from django.contrib.auth.models import User
from django.db.models import Field


class CustomField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.column = 'custom_column'
        self.attname = 'custom_field'


def test_contribute_to_class():
    field = CustomField(verbose_name='Custom Field', name='custom_field')
    
    # Test without private_only
    field.contribute_to_class(User, 'custom_field', private_only=False)
    
    assert hasattr(User, 'custom_field')
    assert isinstance(getattr(User, 'custom_field'), field.descriptor_class)
    
    # Test private_only
    field.contribute_to_class(User, 'custom_field_private', private_only=True)
    
    # Check if a new instance is created for subclasses (not applicable directly here but we can simulate)
    # We will just check if it doesn't overwrite the previous field
    assert hasattr(User, 'custom_field_private')
    assert getattr(User, 'custom_field_private') is not None

    # Check the get_display method when choices are set
    choices_field = CustomField(choices=[(1, 'Choice 1'), (2, 'Choice 2')], name='choice_field')
    choices_field.contribute_to_class(User, 'choice_field', private_only=False)
    
    assert hasattr(User, 'get_choice_field_display')
    assert callable(getattr(User, 'get_choice_field_display'))