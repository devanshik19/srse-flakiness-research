import pytest
from django.contrib.auth.models import User
from django.db import models


class CustomField(models.Field):
    def contribute_to_class(self, cls, name, private_only=False):
        super().contribute_to_class(cls, name, private_only)


def test_contribute_to_class():
    # Arrange
    custom_field = CustomField()
    
    # Act
    custom_field.contribute_to_class(User, 'my_custom_field', private_only=False)

    # Assert
    assert hasattr(User, 'my_custom_field')
    assert isinstance(getattr(User, 'my_custom_field'), CustomField)
    assert User._meta.fields[-1].name == 'my_custom_field'


def test_contribute_to_class_private_only():
    custom_field = CustomField()
    
    # Act
    custom_field.contribute_to_class(User, 'my_private_custom_field', private_only=True)

    # Assert
    assert hasattr(User, 'my_private_custom_field')
    assert isinstance(getattr(User, 'my_private_custom_field'), CustomField)