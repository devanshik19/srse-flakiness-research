import pytest
from django.contrib.auth.models import User
from django.db.models.fields.files import FileField

class TestFileField:
    @pytest.fixture
    def file_field(self):
        return FileField(verbose_name='Test File', name='test_file', upload_to='uploads/', storage=None)

    def test_contribute_to_class(self, file_field):
        user_model = User
        
        # Initially the attribute should not exist
        assert not hasattr(user_model, file_field.attname)

        # Contribute the file field to the user model
        file_field.contribute_to_class(user_model, 'test_file')

        # The attribute should now be added to the user model
        assert hasattr(user_model, file_field.attname)

        # Verify that the descriptor class has been set correctly
        descriptor = getattr(user_model, file_field.attname)
        assert isinstance(descriptor, file_field.descriptor_class)