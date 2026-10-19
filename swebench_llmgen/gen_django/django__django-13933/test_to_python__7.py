import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms import ModelChoiceField

@pytest.fixture
def user_queryset():
    """Fixture to create a queryset of User instances."""
    return User.objects.bulk_create([
        User(username='user1', password='password1'),
        User(username='user2', password='password2'),
    ])

def test_to_python_valid_instance(user_queryset):
    field = ModelChoiceField(queryset=User.objects.all())
    user_instance = User.objects.get(username='user1')
    result = field.to_python(user_instance)
    assert result == user_instance.pk

def test_to_python_valid_id(user_queryset):
    field = ModelChoiceField(queryset=User.objects.all())
    user_instance = User.objects.get(username='user2')
    result = field.to_python(user_instance.pk)
    assert result == user_instance.pk

def test_to_python_invalid_value(user_queryset):
    field = ModelChoiceField(queryset=User.objects.all())
    with pytest.raises(ValidationError):
        field.to_python(999)  # Non-existing user ID

def test_to_python_empty_value(user_queryset):
    field = ModelChoiceField(queryset=User.objects.all())
    result = field.to_python('')
    assert result is None

def test_to_python_invalid_type(user_queryset):
    field = ModelChoiceField(queryset=User.objects.all())
    with pytest.raises(ValidationError):
        field.to_python(object())  # Invalid type