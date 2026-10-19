import pytest
from django.contrib.auth.models import User
from django.db import models

class TestField(models.Field):
    def deconstruct(self):
        return ("test_field", "path.to.TestField", [None], {})

def test_clone():
    field = TestField() 
    cloned_field = field.clone()

    # Check that the cloned field is an instance of the same class
    assert isinstance(cloned_field, TestField)
    
    # Check that cloned field is not the same instance
    assert cloned_field is not field

    # Check that the deconstructed values remain the same
    original_deconstruction = field.deconstruct()
    cloned_deconstruction = cloned_field.deconstruct()

    assert original_deconstruction == cloned_deconstruction