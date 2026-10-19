import pytest
from django import forms
from django.contrib.auth.models import User

class TestBaseForm(forms.BaseForm):
    data = {'username': 'testuser', 'email': 'test@example.com'}
    files = {}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial = {}
        self.changed_data = []

class TestHasChanged:
    
    def test_has_not_changed(self):
        form = TestBaseForm(data={'username': 'testuser', 'email': 'test@example.com'})
        assert not form.has_changed()

    def test_has_changed(self):
        form = TestBaseForm(data={'username': 'testuser', 'email': 'changed@example.com'})
        form.changed_data = ['email']
        assert form.has_changed()

    def test_changed_data_empty(self):
        form = TestBaseForm(data={'username': 'testuser', 'email': 'test@example.com'})
        form.changed_data = []
        assert not form.has_changed()

    def test_changed_data_multiple_fields(self):
        form = TestBaseForm(data={'username': 'changeduser', 'email': 'changed@example.com'})
        form.changed_data = ['username', 'email']
        assert form.has_changed()