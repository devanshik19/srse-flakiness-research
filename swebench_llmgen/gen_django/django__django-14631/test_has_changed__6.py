import pytest
from django import forms
from django.contrib.auth.models import User

class TestBaseForm(forms.BaseForm):
    changed_data = []

    def __init__(self, data=None, initial=None):
        self.data = data or {}
        self.initial = initial or {}
        self.changed_data = self.get_changed_data()

    def get_changed_data(self):
        changed = []
        for key in self.data:
            if self.data[key] != self.initial.get(key):
                changed.append(key)
        return changed

def test_has_changed_no_change():
    initial_data = {'username': 'testuser', 'email': 'test@example.com'}
    form = TestBaseForm(data={'username': 'testuser', 'email': 'test@example.com'}, initial=initial_data)
    assert form.has_changed() is False

def test_has_changed_with_change():
    initial_data = {'username': 'testuser', 'email': 'test@example.com'}
    form = TestBaseForm(data={'username': 'testuser', 'email': 'changed@example.com'}, initial=initial_data)
    assert form.has_changed() is True

def test_has_changed_with_multiple_changes():
    initial_data = {'username': 'testuser', 'email': 'test@example.com'}
    form = TestBaseForm(data={'username': 'changeduser', 'email': 'changed@example.com'}, initial=initial_data)
    assert form.has_changed() is True

def test_has_changed_with_no_data():
    initial_data = {'username': 'testuser', 'email': 'test@example.com'}
    form = TestBaseForm(data={}, initial=initial_data)
    assert form.has_changed() is True

def test_has_changed_with_empty_initial():
    form = TestBaseForm(data={'username': 'testuser', 'email': 'test@example.com'}, initial={})
    assert form.has_changed() is True