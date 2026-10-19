import pytest
from django import forms
from django.contrib.auth.models import User

class TestBaseForm(forms.BaseForm):
    def __init__(self, data=None, initial=None):
        self.changed_data = []
        self.initial = initial or {}
        self.data = data or {}
        self.is_bound = bool(data)

        if self.is_bound:
            self.full_clean()

    def full_clean(self):
        if self.data != self.initial:
            self.changed_data = list(self.data.keys())

def test_has_changed_no_changes():
    form = TestBaseForm(initial={'username': 'testuser'})
    assert not form.has_changed()

def test_has_changed_with_changes():
    form = TestBaseForm(data={'username': 'newuser'}, initial={'username': 'testuser'})
    assert form.has_changed()

def test_has_changed_multiple_fields():
    form = TestBaseForm(data={'username': 'newuser', 'email': 'test@example.com'}, 
                        initial={'username': 'testuser', 'email': 'old@example.com'})
    assert form.has_changed()

def test_has_changed_empty_data():
    form = TestBaseForm(initial={'username': 'testuser'})
    form.data = {}
    form.full_clean()
    assert form.has_changed()