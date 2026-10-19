import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import construct_instance

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

def test_construct_instance_with_all_fields():
    user = User(username='testuser', email='test@example.com', first_name='Test', last_name='User')
    form_data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'first_name': 'NewFirst',
        'last_name': 'NewLast'
    }
    form = UserForm(data=form_data)
    assert form.is_valid()
    
    instance = construct_instance(form, user)
    
    assert instance.username == 'newuser'
    assert instance.email == 'new@example.com'
    assert instance.first_name == 'NewFirst'
    assert instance.last_name == 'NewLast'

def test_construct_instance_with_excluded_fields():
    user = User(username='testuser', email='test@example.com', first_name='Test', last_name='User')
    form_data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'first_name': 'NewFirst',
        'last_name': 'NewLast'
    }
    form = UserForm(data=form_data)
    assert form.is_valid()
    
    instance = construct_instance(form, user, exclude=['email'])
    
    assert instance.username == 'newuser'
    assert instance.email == 'test@example.com'  # Should remain unchanged
    assert instance.first_name == 'NewFirst'
    assert instance.last_name == 'NewLast'

def test_construct_instance_with_fields():
    user = User(username='testuser', email='test@example.com', first_name='Test', last_name='User')
    form_data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'first_name': 'NewFirst',
        'last_name': 'NewLast'
    }
    form = UserForm(data=form_data)
    assert form.is_valid()
    
    instance = construct_instance(form, user, fields=['username', 'first_name'])
    
    assert instance.username == 'newuser'
    assert instance.first_name == 'NewFirst'
    assert instance.email == 'test@example.com'  # Should remain unchanged
    assert instance.last_name == 'User'  # Should remain unchanged

def test_construct_instance_with_default_values():
    user = User(username='testuser', email='test@example.com', first_name='Test', last_name='User')
    form_data = {
        'username': 'testuser',  # No change here
    }
    form = UserForm(data=form_data)
    assert form.is_valid()
    
    instance = construct_instance(form, user)
    
    assert instance.username == 'testuser'  # Unchanged
    assert instance.email == 'test@example.com'  # Unchanged
    assert instance.first_name == 'Test'  # Unchanged
    assert instance.last_name == 'User'  # Unchanged

def test_construct_instance_with_validation_error():
    user = User(username='testuser', email='test@example.com', first_name='Test', last_name='User')
    form_data = {
        'username': '',  # Invalid username
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
    form = UserForm(data=form_data)
    assert not form.is_valid()
    
    with pytest.raises(ValidationError):
        construct_instance(form, user)