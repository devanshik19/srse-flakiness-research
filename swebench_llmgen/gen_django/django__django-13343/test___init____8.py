import pytest
from django.contrib.auth.models import User
from django.db.models.fields.files import FieldFile

def test_field_file_init():
    user = User.objects.create(username='testuser', password='password')
    field = user._meta.get_field('avatar')  # Assuming 'avatar' is a FileField in the User model
    name = 'test_image.jpg'
    
    file_field = FieldFile(user, field, name)
    
    assert file_field.instance == user
    assert file_field.field == field
    assert file_field.storage == field.storage
    assert file_field._committed is True