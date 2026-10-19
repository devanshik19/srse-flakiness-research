import pytest
from django.contrib.auth.models import User
from django.db.models.fields.files import FieldFile
from django.core.files.storage import default_storage

def test_field_file_init():
    # Create a User instance to use as the model instance
    user_instance = User(username='testuser')
    
    # Create a dummy field with default storage
    class DummyField:
        storage = default_storage

    field = DummyField()
    
    # Initialize FieldFile with the user instance, field, and a name
    field_file = FieldFile(instance=user_instance, field=field, name='testfile.txt')
    
    # Assert the initialized attributes
    assert field_file.instance == user_instance
    assert field_file.field == field
    assert field_file.storage == field.storage
    assert field_file._committed is True