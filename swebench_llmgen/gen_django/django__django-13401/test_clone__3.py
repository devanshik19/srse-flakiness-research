import pytest
from django.db.models import Field
from django.contrib.auth.models import User


def test_clone():
    # Create an instance of Field with specific parameters
    field_instance = Field(verbose_name='test_field', name='test', primary_key=False, max_length=100, unique=False, blank=True, null=True)

    # Clone the instance
    cloned_field = field_instance.clone()

    # Ensure that the cloned field is of the same class
    assert isinstance(cloned_field, Field)

    # Ensure that cloned field parameters match the original (excluding name)
    assert cloned_field.verbose_name == field_instance.verbose_name
    assert cloned_field.name != field_instance.name  # name should not be preserved
    assert cloned_field.primary_key == field_instance.primary_key
    assert cloned_field.max_length == field_instance.max_length
    assert cloned_field.unique == field_instance.unique
    assert cloned_field.blank == field_instance.blank
    assert cloned_field.null == field_instance.null

    # Ensure that cloning retains the same internal state without modifying the original
    cloned_field.verbose_name = "changed_field"
    assert cloned_field.verbose_name != field_instance.verbose_name