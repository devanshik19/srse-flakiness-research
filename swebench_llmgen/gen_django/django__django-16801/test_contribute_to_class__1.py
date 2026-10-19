import pytest
from django.contrib.auth.models import User
from django.db.models.fields.files import FileField

class TestFileField:
    def test_contribute_to_class(self):
        file_field = FileField(upload_to='uploads/', storage=None)

        # Simulate a model class
        class TestModel:
            pass

        # Call contribute_to_class
        file_field.contribute_to_class(TestModel, 'test_file')

        # Assert that the attribute is set correctly
        assert hasattr(TestModel, file_field.attname)

        # Check that the descriptor class is properly assigned
        descriptor = getattr(TestModel, file_field.attname)
        assert isinstance(descriptor, file_field.descriptor_class)

        # Check for correct name and class assignment
        assert descriptor.field == file_field