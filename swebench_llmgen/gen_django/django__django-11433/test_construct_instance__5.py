import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

# ModelForm for User
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

# Test for `construct_instance`
def test_construct_instance():
    # Create an instance of the User with some initial data
    user_instance = User(username='testuser', email='test@example.com')

    # Create form data for valid input
    form_data = {
        'username': 'newusername',
        'email': 'newemail@example.com',
        'first_name': 'New',
        'last_name': 'User',
    }
    form = UserForm(data=form_data)

    # Simulate form validation
    assert form.is_valid()

    # Call construct_instance to create a new User instance
    new_user_instance = construct_instance(form, user_instance)

    # Assert that the instance has been updated correctly
    assert new_user_instance.username == 'newusername'
    assert new_user_instance.email == 'newemail@example.com'
    assert new_user_instance.first_name == 'New'
    assert new_user_instance.last_name == 'User'

    # Case where some fields are not provided
    form_data_incomplete = {
        'username': 'incompleteusername',
        'email': '',
    }
    form_incomplete = UserForm(data=form_data_incomplete)

    # Simulate form validation
    assert form_incomplete.is_valid()

    # Call construct_instance to create a new User instance
    incomplete_user_instance = construct_instance(form_incomplete, user_instance)

    # Assert that only provided fields are updated
    assert incomplete_user_instance.username == 'incompleteusername'
    assert incomplete_user_instance.email == 'test@example.com'  # Not updated, as it's empty
    assert incomplete_user_instance.first_name == ''
    assert incomplete_user_instance.last_name == ''

    # Test exclude fields
    form_data_exclude = {
        'username': 'excludedusername',
    }
    form_exclude = UserForm(data=form_data_exclude)

    # Simulate form validation
    assert form_exclude.is_valid()

    # Call construct_instance to create a new User instance
    excluded_user_instance = construct_instance(form_exclude, user_instance, exclude=['email'])

    # Assert that email is untouched
    assert excluded_user_instance.email == 'test@example.com'
    assert excluded_user_instance.username == 'excludedusername'