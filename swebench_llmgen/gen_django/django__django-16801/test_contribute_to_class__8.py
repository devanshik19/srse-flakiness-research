import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.files import FileField

class TestFileField:
    @pytest.fixture
    def file_field(self):
        return FileField()

    @pytest.fixture
    def user_model(self):
        class CustomUser(User):
            file = FileField(upload_to='uploads/')

        return CustomUser

    def test_contribute_to_class(self, file_field, user_model):
        # Act
        file_field.contribute_to_class(user_model, 'file')

        # Assert
        assert hasattr(user_model, file_field.attname)
        descriptor_instance = getattr(user_model, file_field.attname)
        assert isinstance(descriptor_instance, file_field.descriptor_class)

        # Check if backward compatibility is maintained
        assert file_field.description == "File"