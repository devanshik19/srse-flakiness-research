import pytest
from django.forms.models import ModelFormOptions
from django.contrib.auth.models import User

def test_model_form_options_init():
    options = {
        'model': User,
        'fields': ['username', 'email'],
        'exclude': None,
        'widgets': {},
        'localized_fields': None,
        'labels': {},
        'help_texts': {},
        'error_messages': {},
        'field_classes': {}
    }
    
    form_options = ModelFormOptions(options)

    assert form_options.model == User
    assert form_options.fields == ['username', 'email']
    assert form_options.exclude is None
    assert form_options.widgets == {}
    assert form_options.localized_fields is None
    assert form_options.labels == {}
    assert form_options.help_texts == {}
    assert form_options.error_messages == {}
    assert form_options.field_classes == {}