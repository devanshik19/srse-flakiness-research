import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.models import construct_instance

class TestConstructInstanceForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

def test_construct_instance_with_valid_data():
    form_data = {'username': 'testuser', 'email': 'test@example.com'}
    form = TestConstructInstanceForm(data=form_data)
    assert form.is_valid()

    user_instance = User()
    constructed_instance = construct_instance(form, user_instance)

    assert constructed_instance.username == 'testuser'
    assert constructed_instance.email == 'test@example.com'

def test_construct_instance_with_fields():
    form_data = {'username': 'testuser', 'email': 'test@example.com'}
    form = TestConstructInstanceForm(data=form_data)
    assert form.is_valid()

    user_instance = User()
    constructed_instance = construct_instance(form, user_instance, fields=['username'])

    assert constructed_instance.username == 'testuser'
    assert constructed_instance.email != 'test@example.com'  # Email should remain unchanged

def test_construct_instance_with_exclude():
    form_data = {'username': 'testuser', 'email': 'test@example.com'}
    form = TestConstructInstanceForm(data=form_data)
    assert form.is_valid()

    user_instance = User()
    constructed_instance = construct_instance(form, user_instance, exclude=['email'])

    assert constructed_instance.username == 'testuser'
    assert constructed_instance.email != 'test@example.com'  # Email should remain unchanged

def test_construct_instance_with_file_fields():
    # Assuming we modified the User model to include a FileField for the purpose of this test
    # Example: profile_picture = models.FileField(upload_to='profile_pics/', blank=True, null=True)

    form_data = {'username': 'testuser', 'email': 'test@example.com'}
    form = TestConstructInstanceForm(data=form_data)
    assert form.is_valid()

    user_instance = User()
    constructed_instance = construct_instance(form, user_instance)

    assert constructed_instance.username == 'testuser'
    assert constructed_instance.email == 'test@example.com'
    # Test the handling of file fields only if present in the User model

def test_construct_instance_with_empty_form():
    form = TestConstructInstanceForm(data={})

    user_instance = User()
    constructed_instance = construct_instance(form, user_instance)

    assert constructed_instance.username == ''  # Default value
    assert constructed_instance.email == ''  # Default value