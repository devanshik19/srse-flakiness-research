import pytest
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.forms import modelform_factory

def test_modelform_factory_includes_fields():
    UserForm = modelform_factory(User, fields=['username', 'email'])
    form = UserForm()
    assert 'username' in form.fields
    assert 'email' in form.fields
    assert 'password' not in form.fields

def test_modelform_factory_excludes_fields():
    UserForm = modelform_factory(User, exclude=['password'])
    form = UserForm()
    assert 'password' not in form.fields

def test_modelform_factory_with_fields_and_excludes():
    UserForm = modelform_factory(User, fields=['username', 'email', 'password'], exclude=['password'])
    form = UserForm()
    assert 'username' in form.fields
    assert 'email' in form.fields
    assert 'password' not in form.fields

def test_modelform_factory_without_fields_or_excludes():
    with pytest.raises(ImproperlyConfigured):
        modelform_factory(User)

def test_modelform_factory_with_custom_widgets():
    widgets = {
        'username': forms.TextInput(attrs={'class': 'username'}),
        'email': forms.EmailInput(attrs={'class': 'email'}),
    }
    UserForm = modelform_factory(User, widgets=widgets)
    form = UserForm()
    assert isinstance(form.fields['username'].widget, forms.TextInput)
    assert isinstance(form.fields['email'].widget, forms.EmailInput)

def test_modelform_factory_with_custom_labels():
    labels = {
        'username': 'User Name',
        'email': 'Email Address',
    }
    UserForm = modelform_factory(User, labels=labels)
    form = UserForm()
    assert form.fields['username'].label == 'User Name'
    assert form.fields['email'].label == 'Email Address'

def test_modelform_factory_with_custom_help_texts():
    help_texts = {
        'username': 'Your unique username',
        'email': 'Your email address for registration',
    }
    UserForm = modelform_factory(User, help_texts=help_texts)
    form = UserForm()
    assert form.fields['username'].help_text == 'Your unique username'
    assert form.fields['email'].help_text == 'Your email address for registration'

def test_modelform_factory_with_formfield_callback():
    def custom_formfield_callback(field):
        return forms.CharField(label=field.label)

    UserForm = modelform_factory(User, formfield_callback=custom_formfield_callback)
    form = UserForm()
    assert isinstance(form.fields['username'], forms.CharField)
    assert isinstance(form.fields['email'], forms.CharField)