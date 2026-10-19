import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict

def test_model_to_dict_with_all_fields():
    user = User.objects.create_user(username='testuser', password='password', email='test@example.com')
    result = model_to_dict(user)
    assert result['username'] == 'testuser'
    assert result['email'] == 'test@example.com'

def test_model_to_dict_with_fields():
    user = User.objects.create_user(username='testuser', password='password', email='test@example.com')
    result = model_to_dict(user, fields=['username', 'email'])
    assert result == {'username': 'testuser', 'email': 'test@example.com'}

def test_model_to_dict_with_exclude():
    user = User.objects.create_user(username='testuser', password='password', email='test@example.com')
    result = model_to_dict(user, exclude=['email'])
    assert 'email' not in result
    assert result['username'] == 'testuser'

def test_model_to_dict_with_fields_and_exclude():
    user = User.objects.create_user(username='testuser', password='password', email='test@example.com')
    result = model_to_dict(user, fields=['username', 'email'], exclude=['email'])
    assert result == {'username': 'testuser'}
    assert 'email' not in result

def test_model_to_dict_with_no_editable_field():
    class TestModel:
        _meta = type('Meta', (), {'concrete_fields': [], 'private_fields': [], 'many_to_many': []})
        
    instance = TestModel()
    result = model_to_dict(instance)
    assert result == {}
    
def test_model_to_dict_empty_fields_and_exclude():
    user = User.objects.create_user(username='testuser', password='password', email='test@example.com')
    result = model_to_dict(user, fields=[], exclude=[])
    assert result == {}