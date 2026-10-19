import pytest
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

def test_model_to_dict_with_fields():
    user = User.objects.create(username='testuser', email='test@example.com', first_name='Test', last_name='User')
    result = model_to_dict(user, fields=['username', 'email'])
    assert result == {'username': 'testuser', 'email': 'test@example.com'}

def test_model_to_dict_with_exclude():
    user = User.objects.create(username='testuser', email='test@example.com', first_name='Test', last_name='User')
    result = model_to_dict(user, exclude=['email'])
    assert result == {'username': 'testuser', 'first_name': 'Test', 'last_name': 'User'}

def test_model_to_dict_with_both_fields_and_exclude():
    user = User.objects.create(username='testuser', email='test@example.com', first_name='Test', last_name='User')
    result = model_to_dict(user, fields=['username', 'email', 'first_name'], exclude=['first_name'])
    assert result == {'username': 'testuser', 'email': 'test@example.com'}

def test_model_to_dict_without_fields_or_exclude():
    user = User.objects.create(username='testuser', email='test@example.com', first_name='Test', last_name='User')
    result = model_to_dict(user)
    assert result == {
        'id': user.id,
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
    }

def test_model_to_dict_no_editable_fields():
    user = User.objects.create(username='testuser', email='test@example.com', first_name='Test', last_name='User')
    result = model_to_dict(user, fields=['is_active'])
    assert 'is_active' not in result  # is_active is not editable