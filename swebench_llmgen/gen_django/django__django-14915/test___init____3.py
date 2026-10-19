import pytest
from django.contrib.auth.models import User
from django.forms.models import ModelFormOptions

def test_model_form_options_init_with_all_options():
    options = {
        'model': User,
        'fields': ['username', 'email'],
        'exclude': ['password'],
        'widgets': {'username': 'text'},
        'localized_fields': ['username'],
        'labels': {'email': 'Email Address'},
        'help_texts': {'username': 'Enter your username'},
        'error_messages': {'username': {'required': 'This field is required.'}},
        'field_classes': {'username': 'CharField'},
    }
    
    model_form_options = ModelFormOptions(options)
    
    assert model_form_options.model == User
    assert model_form_options.fields == ['username', 'email']
    assert model_form_options.exclude == ['password']
    assert model_form_options.widgets == {'username': 'text'}
    assert model_form_options.localized_fields == ['username']
    assert model_form_options.labels == {'email': 'Email Address'}
    assert model_form_options.help_texts == {'username': 'Enter your username'}
    assert model_form_options.error_messages == {'username': {'required': 'This field is required.'}}
    assert model_form_options.field_classes == {'username': 'CharField'}

def test_model_form_options_init_with_missing_options():
    options = {}
    
    model_form_options = ModelFormOptions(options)
    
    assert model_form_options.model is None
    assert model_form_options.fields is None
    assert model_form_options.exclude is None
    assert model_form_options.widgets is None
    assert model_form_options.localized_fields is None
    assert model_form_options.labels is None
    assert model_form_options.help_texts is None
    assert model_form_options.error_messages is None
    assert model_form_options.field_classes is None