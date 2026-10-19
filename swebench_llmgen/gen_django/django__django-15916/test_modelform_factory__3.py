import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.forms import ModelForm

def test_modelform_factory_all_fields():
    form_class = modelform_factory(User)
    form = form_class()
    
    assert form.is_bound is False
    assert set(form.fields.keys()) == set(User._meta.get_fields())

def test_modelform_factory_specific_fields():
    form_class = modelform_factory(User, fields=['username', 'email'])
    form = form_class()
    
    assert form.is_bound is False
    assert set(form.fields.keys()) == {'username', 'email'}

def test_modelform_factory_exclude_fields():
    form_class = modelform_factory(User, exclude=['password'])
    form = form_class()
    
    assert form.is_bound is False
    assert 'password' not in form.fields

def test_modelform_factory_fields_and_exclude():
    form_class = modelform_factory(User, fields=['username', 'email'], exclude=['password'])
    form = form_class()
    
    assert form.is_bound is False
    assert set(form.fields.keys()) == {'username', 'email'}

def test_modelform_factory_no_fields_or_exclude():
    with pytest.raises(ImproperlyConfigured) as excinfo:
        modelform_factory(User, fields=None, exclude=None)
    assert str(excinfo.value) == ("Calling modelform_factory without defining 'fields' or "
                                   "'exclude' explicitly is prohibited.")

def test_modelform_factory_custom_widget():
    form_class = modelform_factory(User, widgets={'username': forms.TextInput(attrs={'placeholder': 'Enter username'})})
    form = form_class()
    
    assert isinstance(form.fields['username'].widget, forms.TextInput)
    assert form.fields['username'].widget.attrs['placeholder'] == 'Enter username'

def test_modelform_factory_custom_labels():
    labels = {'username': 'User Name'}
    form_class = modelform_factory(User, labels=labels)
    form = form_class()
    
    assert form.fields['username'].label == 'User Name'

def test_modelform_factory_custom_help_texts():
    help_texts = {'username': 'Enter your username'}
    form_class = modelform_factory(User, help_texts=help_texts)
    form = form_class()
    
    assert form.fields['username'].help_text == 'Enter your username'

def test_modelform_factory_custom_error_messages():
    error_messages = {'username': {'required': 'Please enter a username'}}
    form_class = modelform_factory(User, error_messages=error_messages)
    form = form_class()
    
    assert form.error_messages == {'username': {'required': 'Please enter a username'}}

def test_modelform_factory_custom_field_classes():
    field_classes = {'username': forms.CharField}
    form_class = modelform_factory(User, field_classes=field_classes)
    form = form_class()
    
    assert isinstance(form.fields['username'], forms.CharField)