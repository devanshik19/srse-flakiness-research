import pytest
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.db.models.fields import Field

class TestFileField:

    @pytest.fixture
    def file_field(self):
        from django.db.models.fields.files import FileField
        return FileField(upload_to='uploads/', storage=default_storage)

    def test_deconstruct_with_max_length(self, file_field):
        file_field.max_length = 100
        name, path, args, kwargs = file_field.deconstruct()
        assert kwargs.get("max_length") is None
        assert kwargs["upload_to"] == 'uploads/'
        assert kwargs["storage"] == default_storage

    def test_deconstruct_without_max_length(self, file_field):
        file_field.max_length = 200
        name, path, args, kwargs = file_field.deconstruct()
        assert kwargs.get("max_length") == 200
        assert kwargs["upload_to"] == 'uploads/'
        assert kwargs["storage"] == default_storage

    def test_deconstruct_with_custom_storage(self, file_field):
        from django.core.files.storage import FileSystemStorage
        custom_storage = FileSystemStorage()
        file_field.storage = custom_storage
        name, path, args, kwargs = file_field.deconstruct()
        assert kwargs["storage"] == custom_storage