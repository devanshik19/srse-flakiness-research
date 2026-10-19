import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.forms.models import construct_instance


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


def test_construct_instance_with_valid_data():
    user = User(username='testuser')
    form_data = {
        'username': 'newuser',
        'first_name': 'New',
        'last_name': 'Name',
        'email': 'newuser@example.com'
    }
    form = UserForm(data=form_data)
    form.is_valid()
    
    instance = construct_instance(form, user)
    
    assert instance.username == 'newuser'
    assert instance.first_name == 'New'
    assert instance.last_name == 'Name'
    assert instance.email == 'newuser@example.com'


def test_construct_instance_with_fields_parameter():
    user = User(username='testuser')
    form_data = {
        'username': 'newuser',
        'first_name': 'New',
        'last_name': 'Ignored',  # This should be ignored
        'email': 'newuser@example.com'
    }
    form = UserForm(data=form_data)
    form.is_valid()
    
    instance = construct_instance(form, user, fields=['username', 'first_name', 'email'])
    
    assert instance.username == 'newuser'
    assert instance.first_name == 'New'
    assert instance.last_name == 'testuser'  # Should remain unchanged
    assert instance.email == 'newuser@example.com'


def test_construct_instance_with_exclude_parameter():
    user = User(username='testuser')
    form_data = {
        'username': 'newuser',
        'first_name': 'Ignored',  # This should be ignored
        'last_name': 'New',
        'email': 'newuser@example.com'
    }
    form = UserForm(data=form_data)
    form.is_valid()

    instance = construct_instance(form, user, exclude=['first_name'])
    
    assert instance.username == 'newuser'
    assert instance.first_name == 'testuser'  # Should remain unchanged
    assert instance.last_name == 'New'
    assert instance.email == 'newuser@example.com'


def test_construct_instance_with_no_change():
    user = User(username='testuser', first_name='Old', last_name='Name', email='old@example.com')
    form_data = {
        'username': 'testuser',  # No change
        'first_name': 'Old',     # No change
        'last_name': 'Name',     # No change
        'email': 'old@example.com'  # No change
    }
    form = UserForm(data=form_data)
    form.is_valid()
    
    instance = construct_instance(form, user)
    
    assert instance.username == 'testuser'
    assert instance.first_name == 'Old'
    assert instance.last_name == 'Name'
    assert instance.email == 'old@example.com'