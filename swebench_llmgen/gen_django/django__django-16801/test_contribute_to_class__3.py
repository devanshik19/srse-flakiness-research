import pytest
from django.contrib.auth.models import User
from django.db.models import Field

class TestFileField:
    @pytest.fixture
    def file_field(self):
        from django.db.models.fields.files import FileField
        return FileField()

    def test_contribute_to_class(self, file_field):
        user_model = User

        # Check the initial state of the user model
        assert not hasattr(user_model, file_field.attname)

        # Contribute to the user model class
        file_field.contribute_to_class(user_model, 'profile_picture')

        # Check that the attribute has been added to the user model
        assert hasattr(user_model, file_field.attname)

        # Check if the descriptor class is correctly assigned
        descriptor = getattr(user_model, file_field.attname)
        assert isinstance(descriptor, file_field.descriptor_class)