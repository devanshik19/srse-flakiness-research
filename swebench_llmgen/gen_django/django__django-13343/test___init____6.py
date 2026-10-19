import pytest
from django.contrib.auth.models import User
from django.db import models

class FieldFile:
    def __init__(self, instance, field, name):
        super().__init__(None, name)
        self.instance = instance
        self.field = field
        self.storage = field.storage
        self._committed = True

@pytest.mark.parametrize("name", ["test_file", "another_file"])
def test_field_file_init(name):
    user_instance = User(username='testuser')
    field_instance = models.FileField()  # Create a FileField instance for testing

    # Initialize FieldFile
    field_file = FieldFile(user_instance, field_instance, name)

    # Assertions to validate initialization
    assert field_file.instance == user_instance
    assert field_file.field == field_instance
    assert field_file.storage == field_instance.storage
    assert field_file._committed is True