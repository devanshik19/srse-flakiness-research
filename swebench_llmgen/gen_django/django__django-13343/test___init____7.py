import pytest
from django.contrib.auth.models import User
from django.db.models.fields.files import FieldFile

def test_fieldfile_init():
    user = User.objects.create(username='testuser')
    field = User._meta.get_field('username')
    field_file = FieldFile(user, field, 'testfile.txt')
    
    assert field_file.instance == user
    assert field_file.field == field
    assert field_file.storage == field.storage
    assert field_file._committed is True