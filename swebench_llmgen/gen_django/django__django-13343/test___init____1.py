import pytest
from django.contrib.auth.models import User
from django.db.models.fields.files import FieldFile

def test_field_file_init():
    user = User.objects.create(username='testuser', password='password')
    field = user._meta.get_field('avatar')  # Assuming there is a file field named 'avatar'
    name = 'testfile.txt'

    field_file = FieldFile(instance=user, field=field, name=name)

    assert field_file.instance == user
    assert field_file.field == field
    assert field_file.storage == field.storage
    assert field_file._committed is True