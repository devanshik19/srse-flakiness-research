import pytest
from django import forms
from django.contrib.auth.models import User

class TestBaseForm(forms.BaseForm):
    
    def __init__(self, initial=None, data=None):
        self.initial = initial or {}
        self.data = data or {}
        self.changed_data = []
        
        # Simulate the internal state of change tracking based on initial and data
        for key in self.data:
            if key in self.initial and self.data[key] != self.initial[key]:
                self.changed_data.append(key)
            elif key not in self.initial:
                self.changed_data.append(key)

    def has_changed(self):
        """Return True if data differs from initial."""
        return bool(self.changed_data)

def test_has_changed_no_initial_data():
    form = TestBaseForm(data={'username': 'test', 'email': 'test@example.com'})
    assert form.has_changed() is True

def test_has_changed_with_initial_data_same():
    form = TestBaseForm(initial={'username': 'test', 'email': 'test@example.com'},
                        data={'username': 'test', 'email': 'test@example.com'})
    assert form.has_changed() is False

def test_has_changed_with_initial_data_diff():
    form = TestBaseForm(initial={'username': 'test', 'email': 'test@example.com'},
                        data={'username': 'test', 'email': 'changed@example.com'})
    assert form.has_changed() is True

def test_has_changed_with_fields_added():
    form = TestBaseForm(initial={'username': 'test'},
                        data={'username': 'test', 'email': 'test@example.com'})
    assert form.has_changed() is True

def test_has_changed_with_fields_removed():
    form = TestBaseForm(initial={'username': 'test', 'email': 'test@example.com'},
                        data={'username': 'test'})
    assert form.has_changed() is True