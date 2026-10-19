import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField

class TestBoundField:
    class TestField:
        def bound_data(self, data, initial):
            return data or initial

        def prepare_value(self, value):
            return str(value)

    class TestForm(forms.Form):
        username = forms.CharField()

    def test_value_with_bound_form(self):
        form = self.TestForm(data={'username': 'testuser'})
        form.is_bound = True
        field = self.TestField()
        bound_field = BoundField(form=form, field=field, name='username')

        assert bound_field.value() == 'testuser'

    def test_value_with_unbound_form_initial(self):
        form = self.TestForm()
        form.is_bound = False
        field = self.TestField()
        bound_field = BoundField(form=form, field=field, name='username')
        bound_field.initial = 'initialusername'

        assert bound_field.value() == 'initialusername'
        
    def test_value_with_bound_form_no_data(self):
        form = self.TestForm(data={})
        form.is_bound = True
        field = self.TestField()
        bound_field = BoundField(form=form, field=field, name='username')
        bound_field.initial = 'initialusername'

        assert bound_field.value() == 'initialusername'