import pytest
from django.contrib.auth.models import User
from django.forms.models import ModelFormOptions

class TestModelFormOptions:
    
    def test_init_with_all_options(self):
        options = {
            'model': User,
            'fields': ['username', 'email'],
            'exclude': ['password'],
            'widgets': {'username': 'text', 'email': 'email'},
            'localized_fields': [],
            'labels': {'username': 'User Name'},
            'help_texts': {'username': 'Enter your username.'},
            'error_messages': {'username': {'required': 'This field is required.'}},
            'field_classes': {}
        }
        
        form_options = ModelFormOptions(options)
        
        assert form_options.model == User
        assert form_options.fields == ['username', 'email']
        assert form_options.exclude == ['password']
        assert form_options.widgets == {'username': 'text', 'email': 'email'}
        assert form_options.localized_fields == []
        assert form_options.labels == {'username': 'User Name'}
        assert form_options.help_texts == {'username': 'Enter your username.'}
        assert form_options.error_messages == {'username': {'required': 'This field is required.'}}
        assert form_options.field_classes == {}

    def test_init_with_no_options(self):
        form_options = ModelFormOptions()
        
        assert form_options.model is None
        assert form_options.fields is None
        assert form_options.exclude is None
        assert form_options.widgets is None
        assert form_options.localized_fields is None
        assert form_options.labels is None
        assert form_options.help_texts is None
        assert form_options.error_messages is None
        assert form_options.field_classes is None

    def test_init_with_partial_options(self):
        options = {
            'model': User,
            'fields': ['username']
        }
        
        form_options = ModelFormOptions(options)
        
        assert form_options.model == User
        assert form_options.fields == ['username']
        assert form_options.exclude is None
        assert form_options.widgets is None
        assert form_options.localized_fields is None
        assert form_options.labels is None
        assert form_options.help_texts is None
        assert form_options.error_messages is None
        assert form_options.field_classes is None