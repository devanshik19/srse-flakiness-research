import pytest
from django.contrib.auth.models import User
from django.db.models import Field

class TestFieldClone:

    def test_clone(self):
        # Create an instance of Field with some parameters
        original_field = Field(verbose_name='Test Field', name='test_field', primary_key=False, max_length=255)

        # Clone the field
        cloned_field = original_field.clone()

        # Assert that the cloned instance is of the same class
        assert isinstance(cloned_field, Field)

        # Assert that the cloned instance's parameters match the original
        assert cloned_field.verbose_name == original_field.verbose_name
        assert cloned_field.name == original_field.name
        assert cloned_field.primary_key == original_field.primary_key
        assert cloned_field.max_length == original_field.max_length

        # Ensure they are not the same object
        assert cloned_field is not original_field

        # Test cloning with different parameters
        custom_field = Field(verbose_name='Custom Field', name='custom_field', max_length=1000)
        custom_cloned_field = custom_field.clone()

        assert custom_cloned_field.verbose_name == custom_field.verbose_name
        assert custom_cloned_field.name == custom_field.name
        assert custom_cloned_field.max_length == custom_field.max_length
        assert custom_cloned_field is not custom_field