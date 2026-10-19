import pytest
from django.contrib.auth.models import User
from django.db.models import FileField

class TestFileField:
    @pytest.fixture
    def file_field(self):
        return FileField(upload_to='uploads/', storage=None)

    def test_deconstruct_with_max_length(self, file_field):
        file_field.max_length = 100
        name, path, args, kwargs = file_field.deconstruct()
        assert 'max_length' not in kwargs
        assert kwargs['upload_to'] == 'uploads/'
        assert 'storage' not in kwargs

    def test_deconstruct_without_max_length(self, file_field):
        file_field.max_length = 50
        name, path, args, kwargs = file_field.deconstruct()
        assert 'max_length' not in kwargs
        assert kwargs['upload_to'] == 'uploads/'
        assert 'storage' not in kwargs

    def test_deconstruct_with_custom_storage(self, file_field):
        custom_storage = None  # Placeholder for real storage instance
        file_field.storage = custom_storage
        name, path, args, kwargs = file_field.deconstruct()
        assert kwargs['storage'] == custom_storage