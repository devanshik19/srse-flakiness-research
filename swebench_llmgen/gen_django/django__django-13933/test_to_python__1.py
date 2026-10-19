import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms import ModelChoiceField

@pytest.fixture
def user_queryset():
    return User.objects.all()

@pytest.fixture
def model_choice_field(user_queryset):
    return ModelChoiceField(queryset=user_queryset, error_messages={'invalid_choice': 'Invalid choice'})

def test_to_python_valid_instance(model_choice_field, user_queryset):
    user = user_queryset.first()
    value = user.pk  # Test with primary key of an existing user
    result = model_choice_field.to_python(value)
    assert result == user.pk  # Should return the user's primary key

def test_to_python_valid_instance_object(model_choice_field, user_queryset):
    user = user_queryset.first()
    result = model_choice_field.to_python(user)  # Test with user instance
    assert result == user.pk  # Should return the user's primary key

def test_to_python_invalid_choice(model_choice_field):
    with pytest.raises(ValidationError, match='Invalid choice'):
        model_choice_field.to_python(-1)  # Test with non-existent primary key

def test_to_python_empty_value(model_choice_field):
    result = model_choice_field.to_python(None)  # Test with empty value
    assert result is None  # Should return None for empty values