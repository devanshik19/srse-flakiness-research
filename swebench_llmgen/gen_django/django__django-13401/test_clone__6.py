import pytest
from django.contrib.auth.models import User
from django.db.models.fields import Field

def test_clone():
    # Initialize a Field instance
    original_field = Field(verbose_name='Test Field', name='test_field', primary_key=False, 
                            max_length=100, unique=False, blank=False, null=False, 
                            db_index=False, rel=None, default=None, 
                            editable=True, serialize=True, 
                            unique_for_date=None, unique_for_month=None, 
                            unique_for_year=None, choices=None, 
                            help_text='', db_column=None, 
                            db_tablespace=None, auto_created=False, 
                            validators=[], error_messages={})

    # Clone the field
    cloned_field = original_field.clone()

    # Check that the cloned field is an instance of the same class
    assert isinstance(cloned_field, Field)

    # Check that the cloned field has the same properties as the original field
    assert cloned_field.verbose_name == original_field.verbose_name
    assert cloned_field.name == original_field.name
    assert cloned_field.primary_key == original_field.primary_key
    assert cloned_field.max_length == original_field.max_length
    assert cloned_field.unique == original_field.unique
    assert cloned_field.blank == original_field.blank
    assert cloned_field.null == original_field.null
    assert cloned_field.db_index == original_field.db_index
    assert cloned_field.default == original_field.default
    assert cloned_field.editable == original_field.editable
    assert cloned_field.serialize == original_field.serialize
    assert cloned_field.help_text == original_field.help_text

    # Ensure that the cloned field is a different instance
    assert cloned_field is not original_field

    # Also ensure deconstruct does not contain any class attachments
    orig_name, orig_path, orig_args, orig_kwargs = original_field.deconstruct()
    clone_name, clone_path, clone_args, clone_kwargs = cloned_field.deconstruct()
    assert orig_name != clone_name  # They should not be the same since 'name' is not preserved