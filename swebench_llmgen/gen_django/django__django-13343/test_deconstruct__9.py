import pytest
from django.contrib.auth.models import User
from django.db.models import Field
from django.db.models.fields.files import FileField

@pytest.mark.django_db
def test_file_field_deconstruct():
    # Create an instance of the FileField with specific attributes
    file_field = FileField(upload_to='uploads/', storage='custom_storage', max_length=100)

    # Deconstructing the field
    name, path, args, kwargs = file_field.deconstruct()
    
    # Assertions to check the deconstructed values
    assert name == 'file_field'
    assert path == 'django.db.models.fields.files.FileField'
    assert args == []
    
    # Check that max_length is removed if it equals 100
    assert 'max_length' not in kwargs
    
    # Check that upload_to is set correctly
    assert kwargs['upload_to'] == 'uploads/'
    
    # Check if storage is set correctly
    assert kwargs['storage'] == 'custom_storage'  # Ensure custom storage is returned