import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict

def test_model_to_dict_with_fields():
    user = User.objects.create_user(username='testuser', password='password')
    user.first_name = 'Test'
    user.last_name = 'User'
    user.email = 'testuser@example.com'
    user.save()

    result = model_to_dict(user, fields=['username', 'email'])
    expected = {
        'username': 'testuser',
        'email': 'testuser@example.com',
    }
    assert result == expected

def test_model_to_dict_with_exclude():
    user = User.objects.create_user(username='testuser2', password='password')
    user.first_name = 'Example'
    user.last_name = 'User'
    user.email = 'testuser2@example.com'
    user.save()

    result = model_to_dict(user, exclude=['email'])
    expected = {
        'username': 'testuser2',
        'first_name': 'Example',
        'last_name': 'User',
    }
    assert result == expected

def test_model_to_dict_with_both_fields_and_exclude():
    user = User.objects.create_user(username='testuser3', password='password')
    user.first_name = 'Sample'
    user.last_name = 'User'
    user.email = 'testuser3@example.com'
    user.save()

    result = model_to_dict(user, fields=['username', 'email', 'first_name'], exclude=['email'])
    expected = {
        'username': 'testuser3',
        'first_name': 'Sample',
    }
    assert result == expected

def test_model_to_dict_with_no_fields():
    user = User.objects.create_user(username='testuser4', password='password')
    user.first_name = 'Another'
    user.last_name = 'User'
    user.email = 'testuser4@example.com'
    user.save()

    result = model_to_dict(user)
    expected = {
        'username': 'testuser4',
        'first_name': 'Another',
        'last_name': 'User',
        'email': 'testuser4@example.com',
    }
    assert result == expected

def test_model_to_dict_with_no_editable_fields():
    user = User.objects.create_user(username='testuser5', password='password')
    
    # Field that is not editable
    user.is_superuser = False
    user.save()
    
    result = model_to_dict(user, fields=['is_superuser'])
    expected = {}
    assert result == expected