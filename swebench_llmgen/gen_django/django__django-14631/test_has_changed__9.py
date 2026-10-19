import pytest
from django import forms
from django.contrib.auth.models import User

class TestBaseForm(forms.BaseForm):
    def __init__(self, data=None, **kwargs):
        self.changed_data = []
        if data:
            self.changed_data = list(data.keys())
        super().__init__(data=data, **kwargs)

def test_has_changed_initially_no_changes():
    form = TestBaseForm(data={})
    assert not form.has_changed()

def test_has_changed_with_changes():
    form = TestBaseForm(data={'username': 'testuser'})
    assert form.has_changed()

def test_has_changed_with_multiple_fields():
    form = TestBaseForm(data={'username': 'testuser', 'email': 'test@example.com'})
    assert form.has_changed()

def test_has_changed_after_resetting_changes():
    form = TestBaseForm(data={'username': 'testuser'})
    assert form.has_changed()
    
    form.changed_data = []  # Simulating reset of changes
    assert not form.has_changed()