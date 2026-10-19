import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.models import ModelFormOptions

@pytest.mark.parametrize("options, expected_results", [
    ({"model": User, "fields": ['username', 'email'], "exclude": ['password'], 
      "widgets": {}, "localized_fields": None, "labels": {}, 
      "help_texts": {}, "error_messages": {}, "field_classes": {}}, 
      (User, ['username', 'email'], ['password'], {}, None, {}, {}, {}, {})),
    ({"model": None}, (None, None, None, None, None, None, None, None, None)),
    ({"fields": ['username']}, (None, ['username'], None, None, None, None, None, None, None)),
])
def test_model_form_options_init(options, expected_results):
    options_instance = ModelFormOptions(options)
    assert options_instance.model == expected_results[0]
    assert options_instance.fields == expected_results[1]
    assert options_instance.exclude == expected_results[2]
    assert options_instance.widgets == expected_results[3]
    assert options_instance.localized_fields == expected_results[4]
    assert options_instance.labels == expected_results[5]
    assert options_instance.help_texts == expected_results[6]
    assert options_instance.error_messages == expected_results[7]
    assert options_instance.field_classes == expected_results[8]