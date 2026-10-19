import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelFormOptions

def test_model_form_options_init_with_all_attributes():
    options = {
        "model": User,
        "fields": ['username', 'email'],
        "exclude": ['password'],
        "widgets": {},
        "localized_fields": [],
        "labels": {},
        "help_texts": {},
        "error_messages": {},
        "field_classes": {}
    }
    form_options = ModelFormOptions(options)
    
    assert form_options.model == User
    assert form_options.fields == ['username', 'email']
    assert form_options.exclude == ['password']
    assert form_options.widgets == {}
    assert form_options.localized_fields == []
    assert form_options.labels == {}
    assert form_options.help_texts == {}
    assert form_options.error_messages == {}
    assert form_options.field_classes == {}

def test_model_form_options_init_with_partial_attributes():
    options = {
        "model": User,
        "fields": None,
        "exclude": None,
        "widgets": None,
        "localized_fields": None,
        "labels": None,
        "help_texts": None,
        "error_messages": None,
        "field_classes": None
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

def test_model_form_options_init_with_no_attributes():
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