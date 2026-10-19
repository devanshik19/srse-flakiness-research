import pytest
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db.models.fields.files import FieldFile

@pytest.mark.django_db
def test_field_file_init():
    user = User(username='testuser')
    user.save()
    
    field = User._meta.get_field('id')  # Using 'id' field as an example field
    name = 'test_file'

    field_file = FieldFile(instance=user, field=field, name=name)

    assert field_file.instance == user
    assert field_file.field == field
    assert field_file.storage == default_storage
    assert field_file._committed is True