import pytest
from django.db import models
from django.contrib.auth.models import User

# Assuming the FileField is defined with the import provided.
class FileField(models.FileField):
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 100:
            del kwargs["max_length"]
        kwargs["upload_to"] = self.upload_to
        if self.storage is not default_storage:
            kwargs["storage"] = getattr(self, "_storage_callable", self.storage)
        return name, path, args, kwargs

def test_deconstruct_with_max_length():
    field = FileField(upload_to='uploads/', max_length=100)
    name, path, args, kwargs = field.deconstruct()
    
    assert kwargs.get("max_length") is None
    assert kwargs["upload_to"] == 'uploads/'
    assert "storage" not in kwargs

def test_deconstruct_without_max_length():
    field = FileField(upload_to='uploads/', max_length=200)
    name, path, args, kwargs = field.deconstruct()
    
    assert kwargs.get("max_length") == 200
    assert kwargs["upload_to"] == 'uploads/'
    assert "storage" not in kwargs

def test_deconstruct_with_custom_storage():
    custom_storage = models.FileField.storage
    field = FileField(upload_to='uploads/', storage=custom_storage)
    field._storage_callable = lambda: custom_storage
    
    name, path, args, kwargs = field.deconstruct()
    
    assert kwargs["storage"] == custom_storage
    assert kwargs["upload_to"] == 'uploads/'