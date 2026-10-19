import pytest
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import ImproperlyConfigured
from django.forms import modelform_factory

def test_modelform_factory_with_fields():
    UserForm = modelform_factory(User, fields=['username', 'email'])
    form = UserForm(data={'username': 'testuser', 'email': 'test@example.com'})
    assert form.is_valid()
    assert form.cleaned_data['username'] == 'testuser'
    assert form.cleaned_data['email'] == 'test@example.com'

def test_modelform_factory_with_exclude():
    UserForm = modelform_factory(User, exclude=['last_name'])
    form = UserForm(data={'username': 'testuser', 'email': 'test@example.com', 'last_name': 'Doe'})
    assert form.is_valid()
    assert 'last_name' not in form.cleaned_data

def test_modelform_factory_without_fields_or_exclude():
    with pytest.raises(ImproperlyConfigured):
        modelform_factory(User)

def test_modelform_factory_with_widgets():
    widgets = {'username': {'type': 'text'}, 'email': {'type': 'email'}}
    UserForm = modelform_factory(User, fields=['username', 'email'], widgets=widgets)
    form = UserForm()
    assert isinstance(form['username'].widget, dict)
    assert isinstance(form['email'].widget, dict)

def test_modelform_factory_with_labels():
    labels = {'username': 'User Name', 'email': 'Email Address'}
    UserForm = modelform_factory(User, fields=['username', 'email'], labels=labels)
    form = UserForm()
    assert form['username'].label == 'User Name'
    assert form['email'].label == 'Email Address'