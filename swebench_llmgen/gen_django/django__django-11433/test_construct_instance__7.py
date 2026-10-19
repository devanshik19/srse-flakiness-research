import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.utils import ErrorList
from django.db import models

# Define a simple ModelForm for testing
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

# Create a sample user instance for testing
@pytest.fixture
def user_instance():
    return User(username='testuser', email='test@example.com')

def test_construct_instance_with_all_fields(user_instance):
    form_data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'first_name': 'New',
        'last_name': 'User',
    }
    form = UserForm(data=form_data)
    assert form.is_valid()

    instance = construct_instance(form, user_instance)
    assert instance.username == 'newuser'
    assert instance.email == 'new@example.com'
    assert instance.first_name == 'New'
    assert instance.last_name == 'User'

def test_construct_instance_fields_param(user_instance):
    form_data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'first_name': 'New',
        'last_name': 'User',
    }
    form = UserForm(data=form_data)
    assert form.is_valid()

    instance = construct_instance(form, user_instance, fields=['username', 'email'])
    assert instance.username == 'newuser'
    assert instance.email == 'new@example.com'
    assert instance.first_name == 'testuser.first_name'  # should remain unchanged
    assert instance.last_name == 'testuser.last_name'    # should remain unchanged

def test_construct_instance_exclude_param(user_instance):
    form_data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'first_name': 'New',
        'last_name': 'User',
    }
    form = UserForm(data=form_data)
    assert form.is_valid()

    instance = construct_instance(form, user_instance, exclude=['email'])
    assert instance.username == 'newuser'
    assert instance.email == 'test@example.com'  # should remain unchanged
    assert instance.first_name == 'New'
    assert instance.last_name == 'User'

def test_construct_instance_with_non_editable_field(user_instance):
    form_data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'first_name': '',
        'last_name': '',
    }
    form = UserForm(data=form_data)
    assert form.is_valid()

    # Ensure that the instance is constructed correctly
    instance = construct_instance(form, user_instance)
    assert instance.username == 'newuser'
    assert instance.email == 'new@example.com'
    assert instance.first_name == ''  # will be empty as it's non-editable
    assert instance.last_name == ''    # will be empty as it's non-editable

def test_construct_instance_with_file_field(user_instance):
    # This requires a file field in the User model, for demonstration we will simulate it.
    with pytest.raises(Exception):
        # Testing a field that doesn't exist to illustrate; modify accordingly if a FileField is actually utilized.
        form_data = {'username': 'newuser', 'profile_picture': 'fakepath'}
        form = UserForm(data=form_data)
        assert not form.is_valid()