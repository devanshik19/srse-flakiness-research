import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelFormOptions


def test_model_form_options_init_with_all_attributes():
    options = {
        'model': User,
        'fields': ['username', 'email'],
        'exclude': ['password'],
        'widgets': {'username': {'input_type': 'text'}},
        'localized_fields': ['username'],
        'labels': {'username': 'User Name'},
        'help_texts': {'username': 'Enter your username'},
        'error_messages': {'username': {'required': 'This field is required.'}},
        'field_classes': {'username': 'TextInput'},
    }
    
    form_options = ModelFormOptions(options)

    assert form_options.model == User
    assert form_options.fields == options['fields']
    assert form_options.exclude == options['exclude']
    assert form_options.widgets == options['widgets']
    assert form_options.localized_fields == options['localized_fields']
    assert form_options.labels == options['labels']
    assert form_options.help_texts == options['help_texts']
    assert form_options.error_messages == options['error_messages']
    assert form_options.field_classes == options['field_classes']


def test_model_form_options_init_with_none_attributes():
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