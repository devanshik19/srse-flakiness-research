import pytest
from django.db.models import Field
from django.contrib.auth.models import User

def test_clone():
    # Instantiate a Field object
    field_instance = Field(verbose_name='Test Field', name='test_field', primary_key=False, max_length=100)

    # Clone the field instance
    cloned_field = field_instance.clone()

    # Check that the cloned field is an instance of the same class
    assert isinstance(cloned_field, Field)

    # Check that the original field and cloned field have the same attributes
    assert cloned_field.verbose_name == field_instance.verbose_name
    assert cloned_field.name == field_instance.name
    assert cloned_field.primary_key == field_instance.primary_key
    assert cloned_field.max_length == field_instance.max_length

    # Ensure they are not the same instance
    assert cloned_field is not field_instance

    # Test the deconstruct method indirectly through clone by checking if it retains defaults
    deconstructed = field_instance.deconstruct()
    cloned_deconstructed = cloned_field.deconstruct()
    assert deconstructed[0] == cloned_deconstructed[0]  # name
    assert deconstructed[1] == cloned_deconstructed[1]  # path
    assert deconstructed[2] == cloned_deconstructed[2]  # args
    assert deconstructed[3] == cloned_deconstructed[3]  # kwargs