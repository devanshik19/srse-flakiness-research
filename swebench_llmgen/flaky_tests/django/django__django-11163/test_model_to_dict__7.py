import pytest
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

def test_model_to_dict_with_fields():
    user = User.objects.create(username='testuser', email='test@example.com', is_active=True)
    expected_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'is_active': True,
    }
    result = model_to_dict(user, fields=['username', 'email', 'is_active'])
    assert result == expected_data

def test_model_to_dict_with_exclude():
    user = User.objects.create(username='testuser', email='test@example.com', is_active=True)
    expected_data = {
        'username': 'testuser',
        'is_active': True,
    }
    result = model_to_dict(user, exclude=['email'])
    assert result == expected_data

def test_model_to_dict_with_no_fields():
    user = User.objects.create(username='testuser', email='test@example.com', is_active=True)
    result = model_to_dict(user)
    expected_fields = ['username', 'email', 'is_active', 'first_name', 'last_name']
    assert all(field in result for field in expected_fields)

def test_model_to_dict_with_no_editable_fields():
    user = User.objects.create(username='testuser', email='test@example.com', is_active=True)
    User._meta.get_field('is_active').editable = False
    result = model_to_dict(user)
    expected_data = {
        'username': 'testuser',
        'email': 'test@example.com',
    }
    assert result == expected_data

def test_model_to_dict_empty_instance():
    user = User()  # Create an empty User instance
    result = model_to_dict(user)
    expected_data = {
        'username': '',
        'email': '',
        'is_active': False,
    }
    assert result['username'] == expected_data['username']
    assert result['email'] == expected_data['email']
    assert result['is_active'] == expected_data['is_active']