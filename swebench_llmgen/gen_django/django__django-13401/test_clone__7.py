import pytest
from django.contrib.auth.models import User
from django.db.models import Field

def test_clone():
    # Create an instance of the Field class (using appropriate parameters)
    original_field = Field(verbose_name="Test Field", name="test_field", primary_key=False, max_length=255)

    # Clone the original field
    cloned_field = original_field.clone()

    # Assert that the cloned field is an instance of the same class
    assert isinstance(cloned_field, Field)
    
    # Assert that the original and cloned fields are not the same instance
    assert original_field is not cloned_field

    # Assert that the properties of the original match the cloned field
    assert original_field.verbose_name == cloned_field.verbose_name
    assert original_field.name == cloned_field.name
    assert original_field.primary_key == cloned_field.primary_key
    assert original_field.max_length == cloned_field.max_length

    # Ensure that changing the clone does not affect the original
    cloned_field.verbose_name = "Changed Field"
    assert original_field.verbose_name != cloned_field.verbose_name