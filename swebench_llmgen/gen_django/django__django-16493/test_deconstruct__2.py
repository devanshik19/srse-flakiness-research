import pytest
from django.contrib.auth.models import User
from django.db.models import FileField


class CustomFileField(FileField):
    def __init__(self, upload_to=None, storage=None, **kwargs):
        super().__init__(upload_to=upload_to, storage=storage, **kwargs)


@pytest.mark.parametrize("max_length, expected_storage", [
    (100, None),  # max_length is 100, so it should be deleted
    (200, 'default_storage'),  # other max_length should retain storage
])
def test_deconstruct(max_length, expected_storage):
    # Arrange
    field = CustomFileField(upload_to='uploads/', storage='default_storage', max_length=max_length)
    
    # Act
    name, path, args, kwargs = field.deconstruct()

    # Assert
    if max_length == 100:
        assert 'max_length' not in kwargs
    else:
        assert kwargs.get('max_length') == max_length
        
    assert kwargs['upload_to'] == 'uploads/'
    assert kwargs['storage'] == 'default_storage'