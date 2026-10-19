import pytest
from django.forms.models import ModelFormOptions
from django.contrib.auth.models import User

def test_model_form_options_init_with_all_attributes():
    options = {
        "model": User,
        "fields": ["username", "email"],
        "exclude": ["password"],
        "widgets": {"username": None},
        "localized_fields": None,
        "labels": {"username": "Username"},
        "help_texts": {"username": "Enter your username"},
        "error_messages": {"username": {"required": "This field is required."}},
        "field_classes": {"username": None},
    }
    model_form_options = ModelFormOptions(options)

    assert model_form_options.model == User
    assert model_form_options.fields == ["username", "email"]
    assert model_form_options.exclude == ["password"]
    assert model_form_options.widgets == {"username": None}
    assert model_form_options.localized_fields is None
    assert model_form_options.labels == {"username": "Username"}
    assert model_form_options.help_texts == {"username": "Enter your username"}
    assert model_form_options.error_messages == {"username": {"required": "This field is required."}}
    assert model_form_options.field_classes == {"username": None}

def test_model_form_options_init_with_empty_options():
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