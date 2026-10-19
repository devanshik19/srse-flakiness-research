import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelFormOptions

class MockOptions:
    def __init__(self, model=None, fields=None, exclude=None, widgets=None, 
                 localized_fields=None, labels=None, help_texts=None, 
                 error_messages=None, field_classes=None):
        self.model = model
        self.fields = fields
        self.exclude = exclude
        self.widgets = widgets
        self.localized_fields = localized_fields
        self.labels = labels
        self.help_texts = help_texts
        self.error_messages = error_messages
        self.field_classes = field_classes

def test_model_form_options_init():
    # Test with a complete set of options
    options = MockOptions(
        model=User,
        fields=['username', 'email'],
        exclude=['password'],
        widgets={'username': 'text'},
        localized_fields=['username'],
        labels={'username': 'User Name'},
        help_texts={'username': 'Enter your username'},
        error_messages={'username': {'required': 'This field is required.'}},
        field_classes={'username': None}
    )

    form_options = ModelFormOptions(options)

    assert form_options.model == User
    assert form_options.fields == ['username', 'email']
    assert form_options.exclude == ['password']
    assert form_options.widgets == {'username': 'text'}
    assert form_options.localized_fields == ['username']
    assert form_options.labels == {'username': 'User Name'}
    assert form_options.help_texts == {'username': 'Enter your username'}
    assert form_options.error_messages == {'username': {'required': 'This field is required.'}}
    assert form_options.field_classes == {'username': None}

    # Test with no options
    empty_options = MockOptions()
    empty_form_options = ModelFormOptions(empty_options)

    assert empty_form_options.model is None
    assert empty_form_options.fields is None
    assert empty_form_options.exclude is None
    assert empty_form_options.widgets is None
    assert empty_form_options.localized_fields is None
    assert empty_form_options.labels is None
    assert empty_form_options.help_texts is None
    assert empty_form_options.error_messages is None
    assert empty_form_options.field_classes is None