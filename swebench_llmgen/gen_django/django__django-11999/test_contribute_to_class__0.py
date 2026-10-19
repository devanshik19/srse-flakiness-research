import pytest
from django.contrib.auth.models import User
from django.db import models

class TestField(models.Field):
    def contribute_to_class(self, cls, name, private_only=False):
        super().contribute_to_class(cls, name, private_only)

@pytest.mark.django_db
def test_contribute_to_class():
    field = TestField()
    
    # Simulate adding the field to the User model
    field.contribute_to_class(User, 'test_field', private_only=False)
    
    # Check if the field has been added to the User model
    assert hasattr(User, 'test_field')
    
    # Check if the descriptor is an instance of the class
    assert isinstance(getattr(User, 'test_field'), models.fields.Field)
    
    # Check if the field is registered in the model's _meta fields
    assert field in User._meta.fields

    # Test with private_only=True
    field.contribute_to_class(User, 'private_test_field', private_only=True)
    
    # Ensure that the private field has its own instance in subclasses
    assert hasattr(User, 'private_test_field')
    assert isinstance(getattr(User, 'private_test_field'), models.fields.Field)
    
    # Test that default get_<field_name>_display method is created
    if field.choices is not None:
        assert hasattr(User, 'get_test_field_display')
        assert callable(getattr(User, 'get_test_field_display'))

    # Verify the correct registration of the field even with a private field
    assert field in User._meta.fields