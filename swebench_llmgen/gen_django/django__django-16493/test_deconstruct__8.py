import pytest
from django.core.files.storage import default_storage
from django.db import models
from django.contrib.auth.models import User

class FileField(models.FileField):
    def __init__(self, verbose_name=None, name=None, upload_to=None, storage=None, **kwargs):
        super().__init__(verbose_name=verbose_name, name=name, upload_to=upload_to, storage=storage, **kwargs)
        self.upload_to = upload_to
        self._storage_callable = storage

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 100:
            del kwargs["max_length"]
        kwargs["upload_to"] = self.upload_to
        if self.storage is not default_storage:
            kwargs["storage"] = getattr(self, "_storage_callable", self.storage)
        return name, path, args, kwargs

def test_deconstruct_with_max_length():
    field = FileField(max_length=100, upload_to='uploads/')
    
    name, path, args, kwargs = field.deconstruct()
    
    assert kwargs.get("upload_to") == 'uploads/'
    assert "max_length" not in kwargs

def test_deconstruct_without_max_length():
    field = FileField(max_length=200, upload_to='uploads/', storage=default_storage)
    
    name, path, args, kwargs = field.deconstruct()
    
    assert kwargs.get("upload_to") == 'uploads/'
    assert kwargs.get("max_length") == 200

def test_deconstruct_with_custom_storage():
    class CustomStorage:
        pass

    field = FileField(upload_to='uploads/', storage=CustomStorage())
    
    name, path, args, kwargs = field.deconstruct()
    
    assert kwargs.get("upload_to") == 'uploads/'
    assert kwargs.get("storage") == CustomStorage()