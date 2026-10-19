import pytest
from django.contrib.auth.models import User
from django.db.models.fields.files import FileField
from django.core.files.storage import default_storage
from django.db.models.fields.files import FieldFile

@pytest.mark.parametrize("name, expected_committed", [
    ("test_file.txt", True),
    ("another_file.txt", True),
])
def test_fieldfile_init(name, expected_committed):
    user_instance = User(username='testuser')
    field = FileField(storage=default_storage)
    
    # Initialize FieldFile
    field_file = FieldFile(instance=user_instance, field=field, name=name)

    # Assert field file attributes
    assert field_file.instance == user_instance
    assert field_file.field == field
    assert field_file.storage == default_storage
    assert field_file._committed == expected_committed