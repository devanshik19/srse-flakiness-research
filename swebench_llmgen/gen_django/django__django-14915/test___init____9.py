import pytest
from django.contrib.auth.models import User
from django.forms import ModelFormOptions


@pytest.mark.parametrize("options, expected_values", [
    ({"model": User}, {"model": User, "fields": None, "exclude": None,
                       "widgets": None, "localized_fields": None,
                       "labels": None, "help_texts": None,
                       "error_messages": None, "field_classes": None}),
    ({"fields": ["username", "email"]}, {"model": None, "fields": ["username", "email"], 
                                          "exclude": None, "widgets": None,
                                          "localized_fields": None, "labels": None, 
                                          "help_texts": None, "error_messages": None, 
                                          "field_classes": None}),
    ({"exclude": ["password"]}, {"model": None, "fields": None, 
                                   "exclude": ["password"], "widgets": None,
                                   "localized_fields": None, "labels": None, 
                                   "help_texts": None, "error_messages": None, 
                                   "field_classes": None}),
    ({"widgets": {"username": "HiddenInput"}}, {"model": None, "fields": None, 
                                                  "exclude": None, "widgets": {"username": "HiddenInput"},
                                                  "localized_fields": None, "labels": None, 
                                                  "help_texts": None, "error_messages": None, 
                                                  "field_classes": None}),
    ({}, {"model": None, "fields": None, "exclude": None,
           "widgets": None, "localized_fields": None, 
           "labels": None, "help_texts": None,
           "error_messages": None, "field_classes": None}),
])
def test_model_form_options_init(options, expected_values):
    options_instance = ModelFormOptions(options)
    
    assert options_instance.model == expected_values["model"]
    assert options_instance.fields == expected_values["fields"]
    assert options_instance.exclude == expected_values["exclude"]
    assert options_instance.widgets == expected_values["widgets"]
    assert options_instance.localized_fields == expected_values["localized_fields"]
    assert options_instance.labels == expected_values["labels"]
    assert options_instance.help_texts == expected_values["help_texts"]
    assert options_instance.error_messages == expected_values["error_messages"]
    assert options_instance.field_classes == expected_values["field_classes"]