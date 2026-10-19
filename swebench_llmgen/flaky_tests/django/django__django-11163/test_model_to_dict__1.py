import pytest
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

def test_model_to_dict_with_all_fields():
    user = User.objects.create_user(username='testuser', password='password123')
    expected_data = {
        'id': user.id,
        'username': 'testuser',
        'password': user.password,  # This should be a hashed password, so we will focus on the field's presence.
        'first_name': '',
        'last_name': '',
        'email': '',
        'is_staff': False,
        'is_active': True,
        'date_joined': user.date_joined,
    }
    result = model_to_dict(user)
    assert all(item in result.items() for item in expected_data.items())

def test_model_to_dict_with_fields_argument():
    user = User.objects.create_user(username='testuser', password='password123')
    result = model_to_dict(user, fields=['username', 'email'])
    assert result == {'username': 'testuser', 'email': ''}

def test_model_to_dict_with_exclude_argument():
    user = User.objects.create_user(username='testuser', password='password123')
    result = model_to_dict(user, exclude=['username', 'email'])
    assert 'username' not in result
    assert 'email' not in result
    assert 'first_name' in result  # Ensure other fields remain
    assert 'last_name' in result

def test_model_to_dict_with_both_arguments():
    user = User.objects.create_user(username='testuser', password='password123')
    result = model_to_dict(user, fields=['username', 'email'], exclude=['username'])
    assert result == {'email': ''}  # Only the excluded will be missing
    assert 'username' not in result

def test_model_to_dict_without_editable_fields():
    class TestModel:
        _meta = type('Meta', (), {
            'concrete_fields': [],
            'private_fields': [],
            'many_to_many': [],
        })
        def __init__(self):
            pass
    
    instance = TestModel()
    result = model_to_dict(instance)
    assert result == {}