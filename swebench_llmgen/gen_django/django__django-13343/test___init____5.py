import pytest
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db.models.fields.files import FieldFile

class CustomField:
    def __init__(self):
        self.storage = FileSystemStorage()

def test_field_file_init():
    user_instance = User.objects.create_user(username='testuser', password='password')
    custom_field = CustomField()
    field_file = FieldFile(user_instance, custom_field, 'test_file')

    assert field_file.instance == user_instance
    assert field_file.field == custom_field
    assert field_file.storage == custom_field.storage
    assert field_file._committed is True