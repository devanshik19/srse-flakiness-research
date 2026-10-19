import pytest
from django.contrib.auth.models import User
from django.db import models
from django.core.files.storage import FileSystemStorage

class TestFieldFile:
    class DummyField:
        storage = FileSystemStorage()

    def test_init_creates_field_file_instance(self):
        user_instance = User(username='testuser')
        field = self.DummyField()
        name = 'testfile.txt'

        field_file = FieldFile(user_instance, field, name)

        assert field_file.instance == user_instance
        assert field_file.field == field
        assert field_file.storage == field.storage
        assert field_file._committed is True