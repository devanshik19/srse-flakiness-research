import pytest
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

# Assuming FileField is already defined in the same or imported context
class FileField(models.FileField):
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 100:
            del kwargs["max_length"]
        kwargs["upload_to"] = self.upload_to
        if self.storage is not default_storage:
            kwargs["storage"] = getattr(self, "_storage_callable", self.storage)
        return name, path, args, kwargs

@pytest.mark.django_db
def test_file_field_deconstruct():
    # Create an instance of the FileField with specific parameters
    field = FileField(upload_to='uploads/', max_length=100)
    field.storage = default_storage  # Assuming default_storage is used

    # Call the deconstruct method
    name, path, args, kwargs = field.deconstruct()

    # Assertions to check the deconstructed values
    assert name == 'file'  # The default name for FileField in Django
    assert path == 'django.db.models.fields.files.FileField'  # Typical path
    assert args == []
    assert "max_length" not in kwargs  # max_length should be removed
    assert kwargs["upload_to"] == 'uploads/'  # upload_to should be preserved
    assert "storage" not in kwargs  # storage should not be present with default_storage

    # Change storage and test that it correctly reflects in kwargs
    custom_storage = 'custom_storage'
    field._storage_callable = custom_storage
    field.storage = custom_storage
    name, path, args, kwargs = field.deconstruct()

    assert kwargs["storage"] == custom_storage  # storage should be in kwargs now