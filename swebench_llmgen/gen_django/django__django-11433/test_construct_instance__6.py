import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

# Define a simple form for our tests
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

def test_construct_instance_with_valid_data():
    user = User(username='testuser')
    form_data = {'username': 'newuser', 'first_name': 'New', 'last_name': 'User', 'email': 'newuser@example.com'}
    form = UserForm(data=form_data)
    form.is_valid()
    
    constructed_instance = construct_instance(form, user)
    
    assert constructed_instance.username == 'newuser'
    assert constructed_instance.first_name == 'New'
    assert constructed_instance.last_name == 'User'
    assert constructed_instance.email == 'newuser@example.com'

def test_construct_instance_with_excluded_fields():
    user = User(username='testuser', first_name='Test', last_name='User', email='testuser@example.com')
    form_data = {'username': 'excludeduser', 'first_name': 'Excluded'}
    form = UserForm(data=form_data)
    form.is_valid()
    
    constructed_instance = construct_instance(form, user, exclude=['last_name'])
    
    assert constructed_instance.username == 'excludeduser'
    assert constructed_instance.first_name == 'Excluded'
    assert constructed_instance.last_name == 'User'  # Remains unchanged
    assert constructed_instance.email == 'testuser@example.com'  # Remains unchanged

def test_construct_instance_with_fields_param():
    user = User(username='testuser', first_name='Test', last_name='User', email='testuser@example.com')
    form_data = {'username': 'fielduser', 'first_name': 'Field', 'last_name': 'User', 'email': 'fielduser@example.com'}
    form = UserForm(data=form_data)
    form.is_valid()
    
    constructed_instance = construct_instance(form, user, fields=['username', 'first_name'])
    
    assert constructed_instance.username == 'fielduser'
    assert constructed_instance.first_name == 'Field'
    assert constructed_instance.last_name == 'User'  # Remains unchanged
    assert constructed_instance.email == 'testuser@example.com'  # Remains unchanged

def test_construct_instance_with_non_editable_field():
    user = User(username='testuser', first_name='Test', last_name='User', email='testuser@example.com')
    user._meta.get_field('username').editable = False
    form_data = {'username': 'shouldnotchange', 'first_name': 'Test'}
    form = UserForm(data=form_data)
    form.is_valid()
    
    constructed_instance = construct_instance(form, user)
    
    assert constructed_instance.username == 'testuser'  # Should remain unchanged
    assert constructed_instance.first_name == 'Test'  # Should remain unchanged

def test_construct_instance_with_file_field():
    # Assuming a model with a file field (not present in User, but for the sake of testing)
    from django.db import models
    class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        avatar = models.FileField(upload_to='uploads/')
    
    # Create an instance of a Profile with an avatar file field
    profile = Profile(user=User(username='testuser'))
    form_data = {'avatar': 'avatar_file_name.jpg'}
    form = ProfileForm(data=form_data, files={'avatar': 'path/to/avatar_file.jpg'})
    form.is_valid()
    
    constructed_instance = construct_instance(form, profile)
    
    # Assuming a test file handler, we will not validate the file field behavior   
    assert constructed_instance.avatar.name == 'avatar_file_name.jpg'  # Check file field update