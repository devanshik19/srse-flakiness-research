import pytest
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

def test_model_to_dict_with_fields():
    user = User.objects.create(username='testuser', email='test@example.com', is_active=True)
    result = model_to_dict(user, fields=['username', 'email'])
    assert result == {'username': 'testuser', 'email': 'test@example.com'}

def test_model_to_dict_exclude_fields():
    user = User.objects.create(username='testuser', email='test@example.com', is_active=True)
    result = model_to_dict(user, exclude=['email'])
    assert 'email' not in result
    assert result['username'] == 'testuser'

def test_model_to_dict_no_fields():
    user = User.objects.create(username='testuser', email='test@example.com', is_active=True)
    result = model_to_dict(user)
    assert 'username' in result
    assert 'email' in result
    assert 'is_active' in result

def test_model_to_dict_with_editable_and_non_editable_fields():
    user = User.objects.create(username='testuser', email='test@example.com', is_active=True)
    user.is_superuser = True
    user.save()
    result = model_to_dict(user)
    assert 'username' in result
    assert 'is_active' in result
    
    # Non-editable fields should not be included
    assert 'is_superuser' not in result

def test_model_to_dict_empty_fields():
    user = User.objects.create(username='testuser')
    result = model_to_dict(user, fields=[])
    assert result == {}