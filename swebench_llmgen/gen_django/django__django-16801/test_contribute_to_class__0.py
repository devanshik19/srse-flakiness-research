import pytest
from django.contrib.auth.models import User
from django.db.models.fields.files import FileField

class TestFileField:
    @pytest.fixture
    def user_model(self):
        return User

    def test_contribute_to_class(self, user_model):
        file_field = FileField(verbose_name='Test File', name='test_file')
        file_field.contribute_to_class(user_model, 'test_file')

        assert hasattr(user_model, file_field.attname)
        descriptor = getattr(user_model, file_field.attname)
        assert isinstance(descriptor, file_field.descriptor_class)