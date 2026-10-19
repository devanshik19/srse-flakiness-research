import pytest
from django.contrib.auth.models import User
from django.forms.models import ModelFormOptions

def test_model_form_options_init_with_all_options():
    options = {
        'model': User,
        'fields': ['username', 'email'],
        'exclude': ['password'],
        'widgets': {'username': HiddenInput()},
        'localized_fields': ['username'],
        'labels': {'username': 'User Name'},
        'help_texts': {'email': 'Enter your email address.'},
        'error_messages': {'username': {'required': 'This field is required.'}},
        'field_classes': {'username': 'CustomField'},
    }
    
    mfo = ModelFormOptions(options)

    assert mfo.model == User
    assert mfo.fields == ['username', 'email']
    assert mfo.exclude == ['password']
    assert mfo.widgets == {'username': HiddenInput()}
    assert mfo.localized_fields == ['username']
    assert mfo.labels == {'username': 'User Name'}
    assert mfo.help_texts == {'email': 'Enter your email address.'}
    assert mfo.error_messages == {'username': {'required': 'This field is required.'}}
    assert mfo.field_classes == {'username': 'CustomField'}

def test_model_form_options_init_with_no_options():
    mfo = ModelFormOptions()

    assert mfo.model is None
    assert mfo.fields is None
    assert mfo.exclude is None
    assert mfo.widgets is None
    assert mfo.localized_fields is None
    assert mfo.labels is None
    assert mfo.help_texts is None
    assert mfo.error_messages is None
    assert mfo.field_classes is None