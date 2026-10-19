import pytest
from django.contrib.auth.models import User
from django.db.models import Field

@pytest.fixture
def file_field():
    return Field(upload_to='uploads/', storage=default_storage)

def test_deconstruct_with_max_length(file_field):
    # Simulate the max_length scenario
    file_field.max_length = 100
    name, path, args, kwargs = file_field.deconstruct()
    
    assert kwargs.get("max_length") is None  # max_length has been deleted
    assert kwargs["upload_to"] == 'uploads/'  # upload_to is retained

def test_deconstruct_without_max_length(file_field):
    # Simulate the scenario without max_length
    file_field.max_length = None
    name, path, args, kwargs = file_field.deconstruct()
    
    assert "max_length" not in kwargs  # max_length doesn't exist
    assert kwargs["upload_to"] == 'uploads/'  # upload_to is retained

def test_deconstruct_with_custom_storage(file_field):
    class CustomStorage(Storage):
        pass
    
    file_field.storage = CustomStorage()
    name, path, args, kwargs = file_field.deconstruct()

    assert kwargs["storage"] == file_field.storage  # storage is retained