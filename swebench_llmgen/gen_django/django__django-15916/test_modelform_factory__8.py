import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.forms import ModelForm

def test_modelform_factory_with_fields():
    UserForm = modelform_factory(User, fields=['username', 'email'])
    user_form = UserForm()
    assert 'username' in user_form.fields
    assert 'email' in user_form.fields
    assert 'password' not in user_form.fields

def test_modelform_factory_with_exclude():
    UserForm = modelform_factory(User, exclude=['email'])
    user_form = UserForm()
    assert 'email' not in user_form.fields
    assert 'username' in user_form.fields

def test_modelform_factory_with_both_fields_and_exclude():
    UserForm = modelform_factory(User, fields=['username', 'email'], exclude=['username'])
    user_form = UserForm()
    assert 'username' not in user_form.fields
    assert 'email' in user_form.fields

def test_modelform_factory_without_fields_or_exclude():
    with pytest.raises(ImproperlyConfigured):
        modelform_factory(User)

def test_modelform_factory_with_custom_widgets():
    widgets = {
        'username': forms.TextInput(attrs={'class': 'username-class'}),
        'email': forms.EmailInput(attrs={'class': 'email-class'}),
    }
    UserForm = modelform_factory(User, widgets=widgets)
    user_form = UserForm()
    assert isinstance(user_form.fields['username'].widget, forms.TextInput)
    assert user_form.fields['username'].widget.attrs['class'] == 'username-class'
    assert isinstance(user_form.fields['email'].widget, forms.EmailInput)
    assert user_form.fields['email'].widget.attrs['class'] == 'email-class'

def test_modelform_factory_with_labels():
    labels = {
        'username': 'User Name',
        'email': 'Email Address',
    }
    UserForm = modelform_factory(User, labels=labels)
    user_form = UserForm()
    assert user_form.fields['username'].label == 'User Name'
    assert user_form.fields['email'].label == 'Email Address'