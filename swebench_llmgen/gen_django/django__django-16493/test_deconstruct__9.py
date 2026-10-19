import pytest
from django.contrib.auth.models import User
from django.db.models.fields.files import FileField

# Test for FileField's deconstruct method
def test_file_field_deconstruct():
    # Create an instance of FileField with specific parameters
    file_field = FileField(upload_to='uploads/', storage='some_storage', max_length=100)

    # Call the deconstruct method
    name, path, args, kwargs = file_field.deconstruct()

    # Assert the name and path are correct
    assert name == 'file_field'
    assert path == 'django.db.models.fields.files.FileField'

    # Check args are empty
    assert args == []

    # Ensure max_length is not present in kwargs after deconstruction
    assert 'max_length' not in kwargs

    # Check that upload_to is present in kwargs
    assert kwargs['upload_to'] == 'uploads/'

    # Ensure storage is in kwargs (mocking the `_storage_callable` attribute)
    file_field._storage_callable = 'mocked_storage'
    assert kwargs['storage'] == file_field._storage_callable