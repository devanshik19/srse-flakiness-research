import pytest
from django.contrib.auth.models import User
from django.db import models

class CustomField(models.Field):
    def deconstruct(self):
        return self.__class__.__name__, None, [], {}

class Field:
    def __init__(self):
        self.custom_field = CustomField()
        
    def clone(self):
        name, path, args, kwargs = self.custom_field.deconstruct()
        return self.__class__(*args, **kwargs)

def test_clone():
    field_instance = Field()
    cloned_field = field_instance.clone()
    
    # Check that clone is of the same class
    assert isinstance(cloned_field, Field)
    
    # Verify cloned field's attributes and that it is a different instance
    assert cloned_field.custom_field is not field_instance.custom_field
    assert isinstance(cloned_field.custom_field, CustomField)
    assert cloned_field.custom_field.deconstruct() == field_instance.custom_field.deconstruct()

    # Ensure it does not reference the original field
    assert cloned_field.custom_field != field_instance.custom_field