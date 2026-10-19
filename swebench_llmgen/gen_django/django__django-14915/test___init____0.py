import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelFormOptions

def test_model_form_options_init_with_valid_options():
    options = {
        'model': User,
        'fields': ['username', 'email'],
        'exclude': ['password'],
        'widgets': {'username': 'text', 'email': 'email'},
        'localized_fields': ['username'],
        'labels': {'username': 'User Name', 'email': 'Email Address'},
        'help_texts': {'username': 'Enter your user name', 'email': 'Enter your email address'},
        'error_messages': {'username': {'required': 'This field is required.'}},
        'field_classes': {'username': 'CharField'}
    }
    form_options = ModelFormOptions(options)
    
    assert form_options.model == User
    assert form_options.fields == ['username', 'email']
    assert form_options.exclude == ['password']
    assert form_options.widgets == {'username': 'text', 'email': 'email'}
    assert form_options.localized_fields == ['username']
    assert form_options.labels == {'username': 'User Name', 'email': 'Email Address'}
    assert form_options.help_texts == {'username': 'Enter your user name', 'email': 'Enter your email address'}
    assert form_options.error_messages == {'username': {'required': 'This field is required.'}}
    assert form_options.field_classes == {'username': 'CharField'}

def test_model_form_options_init_with_partial_options():
    options = {
        'model': User
    }
    form_options = ModelFormOptions(options)

    assert form_options.model == User
    assert form_options.fields is None
    assert form_options.exclude is None
    assert form_options.widgets is None
    assert form_options.localized_fields is None
    assert form_options.labels is None
    assert form_options.help_texts is None
    assert form_options.error_messages is None
    assert form_options.field_classes is None

def test_model_form_options_init_without_options():
    form_options = ModelFormOptions()

    assert form_options.model is None
    assert form_options.fields is None
    assert form_options.exclude is None
    assert form_options.widgets is None
    assert form_options.localized_fields is None
    assert form_options.labels is None
    assert form_options.help_texts is None
    assert form_options.error_messages is None
    assert form_options.field_classes is None