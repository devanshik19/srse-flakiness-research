import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms import ModelChoiceField

@pytest.fixture
def user_queryset():
    return User.objects.all()

@pytest.fixture
def model_choice_field(user_queryset):
    return ModelChoiceField(queryset=user_queryset)

def test_to_python_valid_instance(model_choice_field, user_queryset):
    user = user_queryset.first()
    # When passing an instance of User
    result = model_choice_field.to_python(user)
    assert result == user.pk

def test_to_python_valid_pk(model_choice_field, user_queryset):
    user = user_queryset.first()
    # When passing a valid primary key
    result = model_choice_field.to_python(user.pk)
    assert result == user.pk

def test_to_python_empty_value(model_choice_field):
    # When passing an empty value
    result = model_choice_field.to_python('')
    assert result is None

def test_to_python_invalid_pk(model_choice_field):
    # When passing an invalid primary key
    with pytest.raises(ValidationError) as excinfo:
        model_choice_field.to_python(999)  # Assuming this PK does not exist
    assert excinfo.value.code == 'invalid_choice'

def test_to_python_invalid_instance(model_choice_field):
    # When passing an invalid instance type
    with pytest.raises(ValidationError) as excinfo:
        model_choice_field.to_python(object())  # Invalid object that is not a User
    assert excinfo.value.code == 'invalid_choice'