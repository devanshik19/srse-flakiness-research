import pytest
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

def test_model_to_dict_with_fields():
    user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
    
    result = model_to_dict(user, fields=['username', 'email'])
    
    assert result == {'username': 'testuser', 'email': 'test@example.com'}

def test_model_to_dict_with_exclude():
    user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
    
    result = model_to_dict(user, exclude=['email'])
    
    assert 'email' not in result
    assert result['username'] == 'testuser'

def test_model_to_dict_with_no_fields():
    user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
    
    result = model_to_dict(user, fields=[])
    
    assert result == {}

def test_model_to_dict_with_no_exclude():
    user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
    
    result = model_to_dict(user, exclude=None)
    
    assert 'username' in result
    assert 'email' in result

def test_model_to_dict_with_no_editable_field():
    class NonEditableUser(User):
        class Meta:
            app_label = 'auth'
            db_table = 'auth_user'

    user = NonEditableUser.objects.create_user(username='testuser', password='testpass', email='test@example.com')
    
    result = model_to_dict(user)

    assert 'password' not in result  # password field is not editable
    assert 'username' in result
    assert 'email' in result