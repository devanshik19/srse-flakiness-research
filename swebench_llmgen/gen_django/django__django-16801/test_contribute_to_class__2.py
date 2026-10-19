import pytest
from django.contrib.auth.models import User
from django.db.models.fields.files import FileField

class TestFileField:

    @pytest.fixture
    def file_field(self):
        return FileField(verbose_name="Test File", name="test_file", upload_to='uploads/', storage=None)

    def test_contribute_to_class(self, file_field):
        user_model = User
        file_field.contribute_to_class(user_model, 'test_file')

        # Check if the attribute is set on the User class
        assert hasattr(user_model, file_field.attname)

        # Check if the descriptor class is correctly set
        descriptor = getattr(user_model, file_field.attname)
        assert isinstance(descriptor, file_field.descriptor_class)

        # Check for the correct attributes in the descriptor
        assert descriptor.field == file_field