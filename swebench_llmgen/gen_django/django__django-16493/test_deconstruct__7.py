import pytest
from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.files import FileField

class CustomFileField(FileField):
    def __init__(self, *args, upload_to='uploads/', **kwargs):
        self.upload_to = upload_to
        super().__init__(*args, **kwargs)

def test_deconstruct_without_max_length():
    field = CustomFileField(max_length=100)
    name, path, args, kwargs = field.deconstruct()
    assert name == 'file'  # Default field name
    assert path == 'django.db.models.fields.files.FileField'
    assert 'max_length' not in kwargs
    assert kwargs['upload_to'] == 'uploads/'
    assert kwargs['storage'] == default_storage

def test_deconstruct_with_custom_storage():
    class CustomStorage:
        pass

    field = CustomFileField(storage=CustomStorage())
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] == CustomStorage()

def test_deconstruct_with_default_storage():
    field = CustomFileField()
    name, path, args, kwargs = field.deconstruct()
    assert 'storage' in kwargs
    assert kwargs['storage'] == default_storage