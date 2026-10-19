import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict

def test_model_to_dict_with_all_fields():
    user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
    
    result = model_to_dict(user)

    assert result['username'] == 'testuser'
    assert result['email'] == 'test@example.com'
    assert 'password' not in result

def test_model_to_dict_with_fields_parameter():
    user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
    
    result = model_to_dict(user, fields=['username', 'email'])

    assert result == {'username': 'testuser', 'email': 'test@example.com'}

def test_model_to_dict_with_exclude_parameter():
    user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
    
    result = model_to_dict(user, exclude=['email'])

    assert result['username'] == 'testuser'
    assert 'email' not in result

def test_model_to_dict_with_fields_and_exclude():
    user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
    
    result = model_to_dict(user, fields=['username', 'email'], exclude=['email'])

    assert result['username'] == 'testuser'
    assert 'email' not in result

def test_model_to_dict_with_no_editable_fields():
    class NonEditableUser(User):
        class Meta:
            fields = ['id']  # Assuming we modify the model's editable fields
        
    user = NonEditableUser.objects.create_user(username='testuser', password='testpass')
    
    result = model_to_dict(user)

    assert result == {}

def test_model_to_dict_with_none_fields_and_exclude():
    user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
    
    result = model_to_dict(user, fields=None, exclude=None)

    assert 'username' in result
    assert 'email' in result