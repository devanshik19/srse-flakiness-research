import pytest
from django.contrib.auth.models import User
from django.forms.models import ModelFormOptions

@pytest.mark.parametrize("options, expected", [
    ({"model": User, "fields": ["username"], "exclude": ["email"], 
      "widgets": {}, "localized_fields": [], 
      "labels": {}, "help_texts": {}, 
      "error_messages": {}, "field_classes": {}}, 
     {"model": User, "fields": ["username"], "exclude": ["email"], 
      "widgets": {}, "localized_fields": [], 
      "labels": {}, "help_texts": {}, 
      "error_messages": {}, "field_classes": {}}),
    ({"model": None}, {"model": None}),
    ({}, {"model": None}),
])
def test_model_form_options_init(options, expected):
    instance = ModelFormOptions(options=options)
    
    assert instance.model == expected["model"]
    assert instance.fields == expected.get("fields", None)
    assert instance.exclude == expected.get("exclude", None)
    assert instance.widgets == expected.get("widgets", None)
    assert instance.localized_fields == expected.get("localized_fields", None)
    assert instance.labels == expected.get("labels", None)
    assert instance.help_texts == expected.get("help_texts", None)
    assert instance.error_messages == expected.get("error_messages", None)
    assert instance.field_classes == expected.get("field_classes", None)