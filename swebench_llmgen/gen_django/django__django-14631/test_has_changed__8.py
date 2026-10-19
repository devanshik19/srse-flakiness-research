import pytest
from django import forms
from django.contrib.auth.models import User

class TestBaseForm(forms.BaseForm):
    initial_data = {'name': 'John', 'email': 'john@example.com'}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial = self.initial_data
        self.changed_data = []

    def is_valid(self):
        # Simulate form validation by checking if the input is different from the initial
        if self.cleaned_data.get('name') != self.initial['name']:
            self.changed_data.append('name')
        if self.cleaned_data.get('email') != self.initial['email']:
            self.changed_data.append('email')
        return not self.changed_data


def test_has_changed_without_changes():
    form = TestBaseForm(data={'name': 'John', 'email': 'john@example.com'})
    form.full_clean()  # Simulate cleaning the form
    assert not form.has_changed()


def test_has_changed_with_changes():
    form = TestBaseForm(data={'name': 'Jane', 'email': 'john@example.com'})
    form.full_clean()  # Simulate cleaning the form
    assert form.has_changed()

    form = TestBaseForm(data={'name': 'John', 'email': 'jane@example.com'})
    form.full_clean()  # Simulate cleaning the form
    assert form.has_changed()

    form = TestBaseForm(data={'name': 'Jane', 'email': 'jane@example.com'})
    form.full_clean()  # Simulate cleaning the form
    assert form.has_changed()