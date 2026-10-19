import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.models import ModelFormOptions

def test_model_form_options_init_with_options():
    options = {
        'model': User,
        'fields': ['username', 'email'],
        'exclude': ['password'],
        'widgets': {'username': None},
        'localized_fields': ['username'],
        'labels': {'username': 'User Name'},
        'help_texts': {'email': 'Enter a valid email address.'},
        'error_messages': {'username': {'required': 'Username is required.'}},
        'field_classes': {}
    }
    form_options = ModelFormOptions(options)

    assert form_options.model == User
    assert form_options.fields == ['username', 'email']
    assert form_options.exclude == ['password']
    assert form_options.widgets == {'username': None}
    assert form_options.localized_fields == ['username']
    assert form_options.labels == {'username': 'User Name'}
    assert form_options.help_texts == {'email': 'Enter a valid email address.'}
    assert form_options.error_messages == {'username': {'required': 'Username is required.'}}
    assert form_options.field_classes == {}

def test_model_form_options_init_with_empty_options():
    options = {}
    form_options = ModelFormOptions(options)

    assert form_options.model is None
    assert form_options.fields is None
    assert form_options.exclude is None
    assert form_options.widgets is None
    assert form_options.localized_fields is None
    assert form_options.labels is None
    assert form_options.help_texts is None
    assert form_options.error_messages is None
    assert form_options.field_classes is None