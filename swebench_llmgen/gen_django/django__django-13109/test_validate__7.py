import pytest
from django.contrib.auth.models import User
from django.core import exceptions
from django.db import models
from .fields.related import ForeignKey

class TestForeignKey(ForeignKey):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class DummyModel(models.Model):
    user_fk = TestForeignKey(to=User, on_delete=models.CASCADE)

def test_validate_when_remote_field_parent_link():
    # Arrange
    field = TestForeignKey(to=User, on_delete=models.CASCADE, parent_link=True)
    # Act
    try:
        field.validate(None, None)
    except exceptions.ValidationError:
        pytest.fail("ValidationError raised unexpectedly")

def test_validate_when_value_is_none():
    # Arrange
    field = TestForeignKey(to=User, on_delete=models.CASCADE)
    model_instance = DummyModel()  # Just to satisfy the model_instance argument
    # Act
    try:
        field.validate(None, model_instance)
    except exceptions.ValidationError:
        pytest.fail("ValidationError raised unexpectedly")

def test_validate_when_value_exists():
    # Arrange
    user = User.objects.create(username='testuser')
    field = TestForeignKey(to=User, on_delete=models.CASCADE)
    model_instance = DummyModel()  # Just to satisfy the model_instance argument
    # Act
    try:
        field.validate(user.pk, model_instance)
    except exceptions.ValidationError:
        pytest.fail("ValidationError raised unexpectedly")

def test_validate_when_value_does_not_exist():
    # Arrange
    field = TestForeignKey(to=User, on_delete=models.CASCADE)
    model_instance = DummyModel()  # Just to satisfy the model_instance argument
    # Act & Assert
    with pytest.raises(exceptions.ValidationError) as excinfo:
        field.validate(99999, model_instance)  # Assuming this ID doesn't exist
    assert 'invalid' in str(excinfo.value)