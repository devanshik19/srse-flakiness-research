import pytest
from django import forms
from django.contrib.auth.models import User

class TestBaseForm(forms.BaseForm):

    def setUp(self):
        self.initial_data = {'username': 'testuser', 'password': 'testpass'}
        self.changed_data = {'username': 'testuser2', 'password': 'testpass'}
        self.form_data = forms.BaseForm(data=self.initial_data)

    def test_has_changed_no_initial_change(self):
        self.form_data.changed_data = []
        assert not self.form_data.has_changed()

    def test_has_changed_with_changes(self):
        self.form_data.changed_data = ['username', 'password']
        assert self.form_data.has_changed()

    def test_has_changed_with_some_changes(self):
        self.form_data.changed_data = ['username']
        assert self.form_data.has_changed()

    def test_has_changed_empty_changed_data(self):
        self.form_data.changed_data = []
        assert not self.form_data.has_changed()

    def test_has_changed_new_field_added(self):
        self.form_data.changed_data = ['new_field']
        assert self.form_data.has_changed()