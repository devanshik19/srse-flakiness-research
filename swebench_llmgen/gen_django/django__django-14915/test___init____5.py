import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.models import ModelFormOptions

@pytest.mark.parametrize("options,expected", [
    (None, (None, None, None, None, None, None, None, None)),
    ({'model': User}, (User, None, None, None, None, None, None, None)),
    ({'fields': ['username']}, (None, ['username'], None, None, None, None, None, None)),
    ({'exclude': ['password']}, (None, None, ['password'], None, None, None, None, None)),
    ({'widgets': {'username': 'text'}}, (None, None, None, {'username': 'text'}, None, None, None, None)),
    ({'localized_fields': ['username']}, (None, None, None, None, ['username'], None, None, None)),
    ({'labels': {'username': 'User Name'}}, (None, None, None, None, None, {'username': 'User Name'}, None, None)),
    ({'help_texts': {'username': 'Enter your username'}}, (None, None, None, None, None, None, {'username': 'Enter your username'}, None)),
    ({'error_messages': {'username': {'required': 'This field is required.'}}}, (None, None, None, None, None, None, None, {'username': {'required': 'This field is required.'}})),
])
def test_model_form_options_init(options, expected):
    options_instance = type('Options', (), options)() if options else None
    form_options = ModelFormOptions(options_instance)

    assert form_options.model == expected[0]
    assert form_options.fields == expected[1]
    assert form_options.exclude == expected[2]
    assert form_options.widgets == expected[3]
    assert form_options.localized_fields == expected[4]
    assert form_options.labels == expected[5]
    assert form_options.help_texts == expected[6]
    assert form_options.error_messages == expected[7]