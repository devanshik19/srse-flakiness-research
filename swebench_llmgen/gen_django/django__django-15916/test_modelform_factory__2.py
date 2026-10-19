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
    UserForm = modelform_factory(User, exclude=['password'])
    form = UserForm(data={'username': 'testuser', 'email': 'test@example.com'})
    assert form.is_valid()

def test_modelform_factory_with_invalid_fields():
    with pytest.raises(ImproperlyConfigured):
        modelform_factory(User)

def test_modelform_factory_with_all_fields():
    UserForm = modelform_factory(User, fields='__all__')
    form = UserForm(data={'username': 'testuser', 'email': 'test@example.com', 'password': 'password'})
    assert form.is_valid()

def test_modelform_factory_with_widgets():
    widgets = {'username': {'type': 'text'}}
    UserForm = modelform_factory(User, fields=['username'], widgets=widgets)
    form = UserForm()
    assert 'username' in form.widgets

def test_modelform_factory_with_help_texts():
    help_texts = {'username': 'Enter your username.'}
    UserForm = modelform_factory(User, fields=['username'], help_texts=help_texts)
    form = UserForm()
    assert form.fields['username'].help_text == 'Enter your username.'

def test_modelform_factory_with_labels():
    labels = {'username': 'User Name'}
    UserForm = modelform_factory(User, fields=['username'], labels=labels)
    form = UserForm()
    assert form.fields['username'].label == 'User Name'

def test_modelform_factory_with_error_messages():
    error_messages = {'username': {'required': 'Username is required.'}}
    UserForm = modelform_factory(User, fields=['username'], error_messages=error_messages)
    form = UserForm(data={})
    assert not form.is_valid()
    assert 'Username is required.' in form.errors['username']

def test_modelform_factory_with_field_classes():
    field_classes = {'username': 'django.forms.CharField'}
    UserForm = modelform_factory(User, fields=['username'], field_classes=field_classes)
    form = UserForm()
    assert isinstance(form.fields['username'], ModelForm.base_fields['username'].field_class)