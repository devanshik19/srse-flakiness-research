import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField

class TestBoundField:

    class TestForm(forms.Form):
        user = forms.ModelChoiceField(queryset=User.objects.all())

    def setup_method(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.form = self.TestForm(data={'user': self.user.pk})
        self.form.is_valid()  # ensure form is valid
        self.bound_field = BoundField(self.form, self.form.fields['user'], 'user')

    def test_data_returns_correct_value(self):
        assert self.bound_field.data() == self.user.pk

    def test_data_returns_none_if_not_given(self):
        empty_form = self.TestForm(data={})
        empty_form.is_valid()  # ensure form is valid
        empty_bound_field = BoundField(empty_form, empty_form.fields['user'], 'user')
        assert empty_bound_field.data() is None