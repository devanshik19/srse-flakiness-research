import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms import ModelChoiceField

@pytest.fixture
def user_queryset():
    return User.objects.bulk_create([
        User(username='user1'),
        User(username='user2'),
        User(username='user3'),
    ])

def test_to_python_valid_choice(user_queryset):
    field = ModelChoiceField(queryset=User.objects.all())
    assert field.to_python('user1') == User.objects.get(username='user1').pk

def test_to_python_invalid_choice(user_queryset):
    field = ModelChoiceField(queryset=User.objects.all())
    with pytest.raises(ValidationError) as excinfo:
        field.to_python('invalid_user')
    assert str(excinfo.value) == field.error_messages['invalid_choice']

def test_to_python_empty_value(user_queryset):
    field = ModelChoiceField(queryset=User.objects.all())
    assert field.to_python('') is None
    assert field.to_python(None) is None

def test_to_python_instance_direct(user_queryset):
    field = ModelChoiceField(queryset=User.objects.all())
    user_instance = User.objects.get(username='user1')
    assert field.to_python(user_instance) == user_instance.pk