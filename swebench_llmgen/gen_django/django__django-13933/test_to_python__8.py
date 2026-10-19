import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms.models import ModelChoiceField

@pytest.fixture
def user_queryset():
    return User.objects.bulk_create([
        User(username='user1'),
        User(username='user2'),
        User(username='user3')
    ])

@pytest.fixture
def model_choice_field(user_queryset):
    queryset = User.objects.all()
    return ModelChoiceField(queryset=queryset)

def test_to_python_with_valid_pk(model_choice_field, user_queryset):
    user1 = User.objects.get(username='user1')
    result = model_choice_field.to_python(user1.pk)
    assert result == user1

def test_to_python_with_valid_instance(model_choice_field, user_queryset):
    user2 = User.objects.get(username='user2')
    result = model_choice_field.to_python(user2)
    assert result == user2

def test_to_python_with_invalid_pk(model_choice_field):
    with pytest.raises(ValidationError):
        model_choice_field.to_python(999)  # Non-existing pk

def test_to_python_with_none_value(model_choice_field):
    result = model_choice_field.to_python(None)
    assert result is None

def test_to_python_with_empty_value(model_choice_field):
    model_choice_field.empty_values = [None, '', ' ']
    result = model_choice_field.to_python('')
    assert result is None