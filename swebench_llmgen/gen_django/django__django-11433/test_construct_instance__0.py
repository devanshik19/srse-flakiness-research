import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, FieldError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.forms.models import construct_instance


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


def test_construct_instance_valid_data():
    user = User(username='testuser', email='test@example.com')
    form_data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'first_name': 'New',
        'last_name': 'User'
    }
    form = UserForm(data=form_data)
    form.is_valid()
    
    instance = construct_instance(form, user)
    
    assert instance.username == 'newuser'
    assert instance.email == 'new@example.com'
    assert instance.first_name == 'New'
    assert instance.last_name == 'User'


def test_construct_instance_with_exclude():
    user = User(username='testuser', email='test@example.com')
    form_data = {
        'username': 'newuser',
        'email': 'new@example.com',
    }
    form = UserForm(data=form_data)
    form.is_valid()

    instance = construct_instance(form, user, exclude=['email'])
    
    assert instance.username == 'newuser'
    assert instance.email == 'test@example.com'  # Email should remain unchanged
    assert instance.first_name == ''  # Default value
    assert instance.last_name == ''  # Default value


def test_construct_instance_with_fields():
    user = User(username='testuser', email='test@example.com')
    form_data = {
        'username': 'newuser'
    }
    form = UserForm(data=form_data)
    form.is_valid()
    
    instance = construct_instance(form, user, fields=['username'])
    
    assert instance.username == 'newuser'
    assert instance.email == 'test@example.com'  # Email remains unchanged
    assert instance.first_name == ''  # Default value
    assert instance.last_name == ''  # Default value


def test_construct_instance_without_field():
    user = User(username='testuser', email='test@example.com')
    form_data = {
        'username': 'newuser',
        'first_name': 'New'
    }
    form = UserForm(data=form_data)
    form.is_valid()
    
    instance = construct_instance(form, user, fields=['username'])
    
    assert instance.username == 'newuser'
    assert instance.email == 'test@example.com'  # Email remains unchanged
    assert instance.first_name == ''  # Default value
    assert instance.last_name == ''  # Default value