import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField

class TestBoundField:
    class TestForm(forms.Form):
        username = forms.CharField(initial='default_user')

    def setup_method(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.form = self.TestForm(data={'username': 'testuser'})
        self.bound_field = BoundField(self.form, self.form.fields['username'], 'username')

    def test_value_with_bound_form(self):
        self.form.is_bound = True
        assert self.bound_field.value() == 'testuser'

    def test_value_with_unbound_form(self):
        self.form.is_bound = False
        assert self.bound_field.value() == 'default_user'

    def test_value_with_empty_data(self):
        self.form = self.TestForm(data={'username': ''})
        self.bound_field = BoundField(self.form, self.form.fields['username'], 'username')
        self.form.is_bound = True
        assert self.bound_field.value() == ''

    def test_value_with_initial_value(self):
        self.form = self.TestForm(data={})
        self.bound_field = BoundField(self.form, self.form.fields['username'], 'username')
        self.form.is_bound = False
        assert self.bound_field.value() == 'default_user'

    def test_value_with_none_data(self):
        self.form = self.TestForm(data={'username': None})
        self.bound_field = BoundField(self.form, self.form.fields['username'], 'username')
        self.form.is_bound = True
        assert self.bound_field.value() is None

    def test_value_with_error(self):
        # Simulate an error scenario where validation fails
        self.form.errors['username'] = ['This field is required.']
        self.bound_field = BoundField(self.form, self.form.fields['username'], 'username')
        self.form.is_bound = True
        assert self.bound_field.value() == 'testuser'