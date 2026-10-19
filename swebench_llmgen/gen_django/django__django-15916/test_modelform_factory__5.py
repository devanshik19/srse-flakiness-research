import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.forms import modelform_factory

def test_modelform_factory_with_fields():
    UserForm = modelform_factory(User, fields=['username', 'email'])
    user_form = UserForm()
    
    assert 'username' in user_form.fields
    assert 'email' in user_form.fields
    assert 'password' not in user_form.fields

def test_modelform_factory_with_exclude():
    UserForm = modelform_factory(User, exclude=['password'])
    user_form = UserForm()
    
    assert 'username' in user_form.fields
    assert 'email' in user_form.fields
    assert 'password' not in user_form.fields

def test_modelform_factory_fields_and_exclude_conflict():
    with pytest.raises(ImproperlyConfigured):
        modelform_factory(User, fields=['username'], exclude=['username'])

def test_modelform_factory_no_fields_or_exclude():
    with pytest.raises(ImproperlyConfigured):
        modelform_factory(User)

def test_modelform_factory_with_widgets():
    widgets = {
        'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
        'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
    }
    UserForm = modelform_factory(User, fields=['username', 'email'], widgets=widgets)
    user_form = UserForm()
    
    assert isinstance(user_form.fields['username'].widget, forms.TextInput)
    assert isinstance(user_form.fields['email'].widget, forms.EmailInput)

def test_modelform_factory_with_labels():
    labels = {
        'username': 'User Name',
        'email': 'Email Address',
    }
    UserForm = modelform_factory(User, fields=['username', 'email'], labels=labels)
    user_form = UserForm()
    
    assert user_form.fields['username'].label == 'User Name'
    assert user_form.fields['email'].label == 'Email Address'

def test_modelform_factory_with_help_texts():
    help_texts = {
        'username': 'Please enter your username.',
        'email': 'Please enter your email address.',
    }
    UserForm = modelform_factory(User, fields=['username', 'email'], help_texts=help_texts)
    user_form = UserForm()
    
    assert user_form.fields['username'].help_text == 'Please enter your username.'
    assert user_form.fields['email'].help_text == 'Please enter your email address.'