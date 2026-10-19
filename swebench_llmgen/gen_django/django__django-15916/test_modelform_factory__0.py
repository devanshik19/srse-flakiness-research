import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.forms import ModelForm
from django.forms.models import modelform_factory

def test_modelform_factory_with_fields():
    UserForm = modelform_factory(User, fields=['username', 'email'])
    form = UserForm()
    
    assert 'username' in form.fields
    assert 'email' in form.fields
    assert 'password' not in form.fields

def test_modelform_factory_with_exclude():
    UserForm = modelform_factory(User, exclude=['password'])
    form = UserForm()
    
    assert 'username' in form.fields
    assert 'email' in form.fields
    assert 'password' not in form.fields

def test_modelform_factory_with_both_fields_and_exclude():
    UserForm = modelform_factory(User, fields=['username', 'email'], exclude=['email'])
    form = UserForm()

    assert 'username' in form.fields
    assert 'email' not in form.fields

def test_modelform_factory_empty_fields_and_exclude():
    with pytest.raises(ImproperlyConfigured):
        modelform_factory(User)

def test_modelform_factory_with_widgets():
    widgets = {
        'username': {'type': 'text'},
        'email': {'type': 'email'},
    }
    UserForm = modelform_factory(User, fields=['username', 'email'], widgets=widgets)
    
    form = UserForm()
    assert isinstance(form.fields['username'].widget, type(widgets['username']))
    assert isinstance(form.fields['email'].widget, type(widgets['email']))

def test_modelform_factory_with_labels():
    labels = {
        'username': 'User Name',
        'email': 'Email Address',
    }
    UserForm = modelform_factory(User, fields=['username', 'email'], labels=labels)
    
    form = UserForm()
    assert form.fields['username'].label == 'User Name'
    assert form.fields['email'].label == 'Email Address'

def test_modelform_factory_with_help_texts():
    help_texts = {
        'username': 'Enter your username.',
        'email': 'Enter your email address.',
    }
    UserForm = modelform_factory(User, fields=['username', 'email'], help_texts=help_texts)
    
    form = UserForm()
    assert form.fields['username'].help_text == 'Enter your username.'
    assert form.fields['email'].help_text == 'Enter your email address.'