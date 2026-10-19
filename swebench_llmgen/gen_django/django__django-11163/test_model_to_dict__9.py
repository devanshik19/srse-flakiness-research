import pytest
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

def test_model_to_dict_with_all_fields():
    user = User.objects.create(username='testuser', password='password123', email='test@example.com')
    result = model_to_dict(user)
    assert result['username'] == 'testuser'
    assert result['email'] == 'test@example.com'
    assert 'password' not in result  # Password should not be included by default

def test_model_to_dict_with_fields():
    user = User.objects.create(username='testuser', password='password123', email='test@example.com')
    result = model_to_dict(user, fields=['username', 'email'])
    assert result['username'] == 'testuser'
    assert result['email'] == 'test@example.com'
    assert 'password' not in result  # Ensures password is not included

def test_model_to_dict_with_exclude():
    user = User.objects.create(username='testuser', password='password123', email='test@example.com')
    result = model_to_dict(user, exclude=['email'])
    assert result['username'] == 'testuser'
    assert 'email' not in result  # email should be excluded

def test_model_to_dict_with_fields_and_exclude():
    user = User.objects.create(username='testuser', password='password123', email='test@example.com')
    result = model_to_dict(user, fields=['username', 'email'], exclude=['email'])
    assert result['username'] == 'testuser'
    assert 'email' not in result  # email should be excluded even though in fields