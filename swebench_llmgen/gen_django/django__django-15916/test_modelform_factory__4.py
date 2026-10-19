import pytest
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import ImproperlyConfigured
from django.forms import modelform_factory

def test_modelform_factory_with_fields():
    UserForm = modelform_factory(User, fields=['username', 'password'])
    assert UserForm.base_fields['username'].label == 'Username'
    assert UserForm.base_fields['password'].label == 'Password'

def test_modelform_factory_with_exclude():
    UserForm = modelform_factory(User, exclude=['last_login'])
    assert 'last_login' not in UserForm.base_fields

def test_modelform_factory_with_widgets():
    UserForm = modelform_factory(User, widgets={'password': {'type': 'password'}})
    assert isinstance(UserForm.base_fields['password'].widget, type(UserForm.base_fields['password'].widget))

def test_modelform_factory_without_fields_or_exclude():
    with pytest.raises(ImproperlyConfigured):
        modelform_factory(User)

def test_modelform_factory_with_custom_labels():
    labels = {'username': 'User Name', 'password': 'User Password'}
    UserForm = modelform_factory(User, labels=labels)
    assert UserForm.base_fields['username'].label == 'User Name'
    assert UserForm.base_fields['password'].label == 'User Password'

def test_modelform_factory_with_field_classes():
    from django.forms.fields import CharField
    field_classes = {'username': CharField}
    UserForm = modelform_factory(User, field_classes=field_classes)
    assert isinstance(UserForm.base_fields['username'], CharField)

def test_modelform_factory_with_help_texts():
    help_texts = {'username': 'Enter your username'}
    UserForm = modelform_factory(User, help_texts=help_texts)
    assert UserForm.base_fields['username'].help_text == 'Enter your username'