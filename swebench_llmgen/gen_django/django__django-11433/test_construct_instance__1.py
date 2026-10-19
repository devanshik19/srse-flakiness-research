import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

# Define a simple form that uses the User model
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

def test_construct_instance():
    # Create a User instance
    user_instance = User(username='testuser', first_name='Test', last_name='User', email='test@example.com')
    
    # Create a bound form with valid data
    form_data = {'username': 'newuser', 'first_name': 'New', 'last_name': 'User', 'email': 'new@example.com'}
    form = UserForm(data=form_data, instance=user_instance)
    
    # Validate the form
    assert form.is_valid()
    
    # Construct an instance using the focal function
    new_instance = construct_instance(form, user_instance)

    # Verify that the instance has been updated correctly
    assert new_instance.username == 'newuser'
    assert new_instance.first_name == 'New'
    assert new_instance.last_name == 'User'  # last_name should not change since it is not in form_data
    assert new_instance.email == 'new@example.com'

def test_construct_instance_with_exclude():
    user_instance = User(username='testuser', first_name='Test', last_name='User', email='test@example.com')
    
    form_data = {'username': 'excludeduser', 'email': 'excluded@example.com'}
    form = UserForm(data=form_data, instance=user_instance)
    
    assert form.is_valid()
    
    # Construct an instance excluding 'last_name'
    new_instance = construct_instance(form, user_instance, exclude=['last_name'])

    assert new_instance.username == 'excludeduser'
    assert new_instance.first_name == 'Test'  # Should not change
    assert new_instance.last_name == 'User'    # Should remain unchanged since we excluded it
    assert new_instance.email == 'excluded@example.com'

def test_construct_instance_with_fields():
    user_instance = User(username='testuser', first_name='Test', last_name='User', email='test@example.com')
    
    form_data = {'username': 'fielduser', 'first_name': 'Field', 'email': 'field@example.com'}
    form = UserForm(data=form_data, instance=user_instance)
    
    assert form.is_valid()
    
    # Construct an instance with specified fields
    new_instance = construct_instance(form, user_instance, fields=['username', 'first_name'])

    assert new_instance.username == 'fielduser'
    assert new_instance.first_name == 'Field'
    assert new_instance.last_name == 'User'  # Should remain unchanged
    assert new_instance.email == 'test@example.com'  # Should remain unchanged