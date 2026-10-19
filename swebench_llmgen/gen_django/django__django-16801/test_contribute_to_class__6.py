import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.files import FileField

class TestFileField:

    @pytest.fixture
    def file_field(self):
        return FileField(verbose_name='Test File', name='test_file', upload_to='uploads/', storage=None)

    @pytest.fixture
    def user_model(self, file_field):
        class UserWithFileField(User):
            test_file = file_field

        return UserWithFileField

    def test_contribute_to_class(self, user_model, file_field):
        # Check the field is properly added to the user model
        assert hasattr(user_model, file_field.attname)
        descriptor = getattr(user_model, file_field.attname)
        assert isinstance(descriptor, file_field.descriptor_class)

        # Verify that the descriptor class was set correctly
        assert descriptor.field is file_field

        # Check class-level attributes
        assert user_model._meta.get_field(file_field.attname) is file_field
        assert file_field.description == 'Test File'