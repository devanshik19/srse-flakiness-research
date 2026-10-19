import pytest
from django.contrib.auth.models import User
from django.db.models.fields.files import FileField

class TestFileField:

    def test_deconstruct_with_max_length(self):
        field = FileField(max_length=100, upload_to='uploads/')
        name, path, args, kwargs = field.deconstruct()
        
        assert name == 'file'
        assert path == 'django.db.models.fields.files.FileField'
        assert args == []
        assert 'max_length' not in kwargs
        assert kwargs['upload_to'] == 'uploads/'
        assert 'storage' not in kwargs

    def test_deconstruct_without_max_length(self):
        field = FileField(max_length=200, upload_to='uploads/')
        name, path, args, kwargs = field.deconstruct()
        
        assert name == 'file'
        assert path == 'django.db.models.fields.files.FileField'
        assert args == []
        assert kwargs['max_length'] == 200
        assert kwargs['upload_to'] == 'uploads/'
        assert 'storage' not in kwargs

    def test_deconstruct_with_custom_storage(self):
        class CustomStorage:
            pass

        storage = CustomStorage()
        field = FileField(storage=storage, upload_to='uploads/')
        field._storage_callable = storage
        name, path, args, kwargs = field.deconstruct()
        
        assert name == 'file'
        assert path == 'django.db.models.fields.files.FileField'
        assert args == []
        assert kwargs['upload_to'] == 'uploads/'
        assert kwargs['storage'] == storage