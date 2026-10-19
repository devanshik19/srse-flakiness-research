import pytest
from django.core.files.storage import default_storage
from django.db.models import Field
from django.contrib.auth.models import User

class FileField(Field):
    def __init__(self, verbose_name=None, name=None, upload_to='', storage=default_storage, **kwargs):
        super().__init__(verbose_name, name, **kwargs)
        self.upload_to = upload_to
        self.storage = storage

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 100:
            del kwargs["max_length"]
        kwargs['upload_to'] = self.upload_to
        if self.storage is not default_storage:
            kwargs['storage'] = self.storage
        return name, path, args, kwargs

@pytest.fixture
def file_field():
    return FileField(upload_to='uploads/', storage=default_storage)

def test_deconstruct_default_storage(file_field):
    name, path, args, kwargs = file_field.deconstruct()
    assert kwargs['upload_to'] == 'uploads/'
    assert 'storage' not in kwargs

def test_deconstruct_custom_storage(file_field):
    custom_storage = None  # Replace with an actual Storage instance if required
    file_field.storage = custom_storage
    name, path, args, kwargs = file_field.deconstruct()
    assert kwargs['upload_to'] == 'uploads/'
    assert kwargs['storage'] == custom_storage

def test_deconstruct_max_length(file_field):
    field_with_max_length = FileField(max_length=100, upload_to='uploads/')
    name, path, args, kwargs = field_with_max_length.deconstruct()
    assert 'max_length' not in kwargs