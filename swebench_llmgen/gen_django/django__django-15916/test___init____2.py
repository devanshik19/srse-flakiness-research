import pytest
from django.forms.models import ModelFormOptions
from django.contrib.auth.models import User

def test_model_form_options_init():
    # Test with default options
    options = type('Options', (object,), {})()
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

    # Test with partial options
    options.model = User
    options.fields = ['username', 'email']
    options.exclude = ['password']
    options.widgets = {'username': 'text', 'email': 'email'}
    
    form_options = ModelFormOptions(options)
    assert form_options.model == User
    assert form_options.fields == ['username', 'email']
    assert form_options.exclude == ['password']
    assert form_options.widgets == {'username': 'text', 'email': 'email'}
    
    # Test with all options
    options.localized_fields = ['username']
    options.labels = {'username': 'User Name'}
    options.help_texts = {'email': 'Please provide a valid email.'}
    options.error_messages = {'invalid': 'This field is invalid.'}
    options.field_classes = {'username': 'TextInput'}

    form_options = ModelFormOptions(options)
    assert form_options.localized_fields == ['username']
    assert form_options.labels == {'username': 'User Name'}
    assert form_options.help_texts == {'email': 'Please provide a valid email.'}
    assert form_options.error_messages == {'invalid': 'This field is invalid.'}
    assert form_options.field_classes == {'username': 'TextInput'}