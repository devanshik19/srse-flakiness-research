import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.files import FileField

class TestFileField:
    @pytest.fixture
    def file_field(self):
        return FileField(upload_to='uploads/', storage=None)

    def test_contribute_to_class(self, file_field):
        class TestModel:
            pass

        file_field.contribute_to_class(TestModel, 'file_field')

        # Check if the attribute is set on the TestModel
        assert hasattr(TestModel, 'file_field')
        # Check if the attribute is an instance of the descriptor class
        assert isinstance(getattr(TestModel, 'file_field'), file_field.descriptor_class)
        
        # Test if the attribute name is correct
        assert file_field.attname == 'file_field'