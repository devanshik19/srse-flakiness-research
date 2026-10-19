import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms import ModelChoiceField

def test_to_python_with_valid_value():
    user = User.objects.create(username='testuser')
    field = ModelChoiceField(queryset=User.objects.all())
    
    result = field.to_python(user.pk)
    
    assert result == user.pk

def test_to_python_with_instance():
    user = User.objects.create(username='testuser')
    field = ModelChoiceField(queryset=User.objects.all())
    
    result = field.to_python(user)
    
    assert result == user.pk

def test_to_python_with_invalid_value():
    field = ModelChoiceField(queryset=User.objects.all())
    
    with pytest.raises(ValidationError) as excinfo:
        field.to_python(999)  # non-existent user pk
    
    assert excinfo.value.code == 'invalid_choice'

def test_to_python_with_none_value():
    field = ModelChoiceField(queryset=User.objects.all())
    
    result = field.to_python(None)
    
    assert result is None

def test_to_python_with_empty_value():
    field = ModelChoiceField(queryset=User.objects.all())
    field.empty_values = {None, '', ' '}

    result = field.to_python('')
    
    assert result is None