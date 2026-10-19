import pytest
from django.contrib.auth.models import User
from itertools import chain
from django.core.exceptions import FieldError, ValidationError
from django.forms.models import model_to_dict

def test_model_to_dict_all_fields():
    user = User.objects.create_user(username='testuser', password='testpass')
    expected_data = {
        'id': user.id,
        'username': 'testuser',
        'first_name': '',
        'last_name': '',
        'email': '',
        'is_staff': False,
        'is_active': True,
        'is_superuser': False,
        'last_login': None,
        'date_joined': user.date_joined,
    }
    
    data = model_to_dict(user)
    
    assert data == expected_data

def test_model_to_dict_with_fields():
    user = User.objects.create_user(username='testuser', password='testpass')
    expected_data = {
        'username': 'testuser',
        'email': '',
    }
    
    data = model_to_dict(user, fields=['username', 'email'])
    
    assert data == expected_data

def test_model_to_dict_with_exclude():
    user = User.objects.create_user(username='testuser', password='testpass')
    expected_data = {
        'id': user.id,
        'username': 'testuser',
        'first_name': '',
        'last_name': '',
        'email': '',
        'is_superuser': False,
        'is_active': True,
        'is_staff': False,
        'last_login': None,
        'date_joined': user.date_joined,
    }
    
    data = model_to_dict(user, exclude=['password', 'is_superuser'])
    
    assert data == expected_data
    assert 'password' not in data
    assert 'is_superuser' not in data

def test_model_to_dict_with_fields_and_exclude():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
    expected_data = {
        'username': 'testuser',
    }
    
    data = model_to_dict(user, fields=['username', 'email'], exclude=['email'])
    
    assert data == expected_data
    assert 'email' not in data