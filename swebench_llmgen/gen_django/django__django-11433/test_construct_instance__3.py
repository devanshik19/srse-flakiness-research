import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

# Define a form for the User model
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

def test_construct_instance_valid_data():
    form_data = {
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testuser@example.com'
    }
    form = UserForm(data=form_data)
    assert form.is_valid()
    user_instance = User()
    
    result_instance = construct_instance(form, user_instance)
    
    assert result_instance.username == 'testuser'
    assert result_instance.first_name == 'Test'
    assert result_instance.last_name == 'User'
    assert result_instance.email == 'testuser@example.com'

def test_construct_instance_with_exclude():
    form_data = {
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testuser@example.com'
    }
    form = UserForm(data=form_data)
    assert form.is_valid()
    user_instance = User(username='oldusername', email='old@example.com')
    
    result_instance = construct_instance(form, user_instance, exclude=['email'])
    
    assert result_instance.username == 'testuser'
    assert result_instance.first_name == 'Test'
    assert result_instance.last_name == 'User'
    assert result_instance.email == 'old@example.com'  # email not updated

def test_construct_instance_with_fields():
    form_data = {
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testuser@example.com'
    }
    form = UserForm(data=form_data)
    assert form.is_valid()
    user_instance = User()
    
    result_instance = construct_instance(form, user_instance, fields=['username', 'email'])
    
    assert result_instance.username == 'testuser'
    assert result_instance.first_name is None  # not included in fields
    assert result_instance.last_name is None  # not included in fields
    assert result_instance.email == 'testuser@example.com'

def test_construct_instance_with_no_editable_field():
    form_data = {
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testuser@example.com'
    }
    form = UserForm(data=form_data)
    assert form.is_valid()
    user_instance = User(username='previoususer', email='previous@example.com')
    
    result_instance = construct_instance(form, user_instance)

    assert result_instance.username == 'testuser'
    assert result_instance.email == 'testuser@example.com'
    assert result_instance.first_name == 'Test'
    assert result_instance.last_name == 'User'

def test_construct_instance_no_change_in_default():
    user_instance = User(username='testuser', email='testuser@example.com')  # Default set
    form_data = {
        'username': 'testuser',  # same as existing
        'first_name': '',  # Empty field won't change previous value
        'last_name': '',  # Empty field won't change previous value
        'email': '',  # Empty field won't change previous value
    }
    form = UserForm(data=form_data)
    assert form.is_valid()
    
    result_instance = construct_instance(form, user_instance)

    assert result_instance.username == 'testuser'
    assert result_instance.first_name == ''
    assert result_instance.last_name == ''
    assert result_instance.email == 'testuser@example.com'  # Default should remain