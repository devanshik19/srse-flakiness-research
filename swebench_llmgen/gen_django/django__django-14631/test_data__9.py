import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField

class TestBoundFieldData:
    class TestForm(forms.Form):
        username = forms.CharField()

    def setup_method(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.form = self.TestForm(data={'username': 'testuser'})
        self.form.is_valid()  # Validate the form to populate _field_data_value

        self.bound_field = BoundField(self.form, self.form.fields['username'], 'username')

    def test_data_returns_correct_value(self):
        # Test returns the correct value when data is provided.
        assert self.bound_field.data() == 'testuser'

    def test_data_returns_none_when_not_given(self):
        # Test returns None when no data was given.
        empty_form = self.TestForm(data={})
        empty_bound_field = BoundField(empty_form, empty_form.fields['username'], 'username')
        assert empty_bound_field.data() is None