import pytest
from django.forms.models import ModelFormOptions
from django.contrib.auth.models import User

def test_model_form_options_init_with_only_model():
    options = type('Options', (object,), {'model': User})()
    mfo = ModelFormOptions(options)
    assert mfo.model == User
    assert mfo.fields is None
    assert mfo.exclude is None
    assert mfo.widgets is None
    assert mfo.localized_fields is None
    assert mfo.labels is None
    assert mfo.help_texts is None
    assert mfo.error_messages is None
    assert mfo.field_classes is None

def test_model_form_options_init_with_all_attributes():
    options = type('Options', (object,), {
        'model': User,
        'fields': ['username', 'email'],
        'exclude': ['password'],
        'widgets': {},
        'localized_fields': [],
        'labels': {'username': 'User Name'},
        'help_texts': {'email': 'Enter a valid email address.'},
        'error_messages': {},
        'field_classes': {}
    })()
    mfo = ModelFormOptions(options)
    assert mfo.model == User
    assert mfo.fields == ['username', 'email']
    assert mfo.exclude == ['password']
    assert mfo.widgets == {}
    assert mfo.localized_fields == []
    assert mfo.labels == {'username': 'User Name'}
    assert mfo.help_texts == {'email': 'Enter a valid email address.'}
    assert mfo.error_messages == {}
    assert mfo.field_classes == {}

def test_model_form_options_init_with_empty_options():
    options = type('Options', (object,), {})()
    mfo = ModelFormOptions(options)
    assert mfo.model is None
    assert mfo.fields is None
    assert mfo.exclude is None
    assert mfo.widgets is None
    assert mfo.localized_fields is None
    assert mfo.labels is None
    assert mfo.help_texts is None
    assert mfo.error_messages is None
    assert mfo.field_classes is None