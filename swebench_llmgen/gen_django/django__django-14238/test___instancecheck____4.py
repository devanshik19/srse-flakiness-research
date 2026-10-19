import pytest
from django.contrib.auth.models import User
from django.db.models.fields import AutoFieldMeta

class CustomModel(AutoFieldMeta):
    @property
    def _subclasses(self):
        return (User,)

def test_instancecheck_with_valid_instance():
    custom_meta = CustomModel()
    user_instance = User(username='testuser')
    
    assert custom_meta.__instancecheck__(user_instance) is True

def test_instancecheck_with_invalid_instance():
    custom_meta = CustomModel()
    invalid_instance = object()  # Not a User instance
    
    assert custom_meta.__instancecheck__(invalid_instance) is False