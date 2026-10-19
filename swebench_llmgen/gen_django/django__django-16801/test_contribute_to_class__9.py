import pytest
from django.contrib.auth.models import User
from django.db.models import Field
from django.core.files.storage import default_storage
from django.core.files.base import File
from django.db.models.fields.files import FileField


@pytest.fixture
def file_field():
    return FileField(verbose_name='Test File', name='test_file', upload_to='uploads/', storage=default_storage)


@pytest.fixture
def user_model():
    return User(username='testuser', password='password')


def test_contribute_to_class(file_field, user_model):
    # Simulate contributing the FileField to the User model
    file_field.contribute_to_class(User, 'test_file_field')

    # Check if the attribute is set on the User model
    assert hasattr(User, 'test_file_field')
    
    # Check if it is an instance of the expected descriptor class
    descriptor = getattr(User, 'test_file_field')
    assert isinstance(descriptor, Field)  # Ensure it's a Field descriptor

    # Check that the descriptor is properly initialized with the correct FileField
    assert descriptor.field is file_field