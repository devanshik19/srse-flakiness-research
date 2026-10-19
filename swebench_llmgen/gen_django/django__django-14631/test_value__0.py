import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField

class TestBoundFieldValue:
    class TestForm(forms.Form):
        name = forms.CharField(initial='John Doe')

    def setup_method(self):
        self.form = self.TestForm(data={'name': 'Jane Doe'})
        self.bound_field = BoundField(self.form, self.form.fields['name'], 'name')

    def test_value_initial(self):
        """Test value when the form is not bound."""
        self.form = self.TestForm(data={})  # Unbound form
        bound_field = BoundField(self.form, self.form.fields['name'], 'name')
        assert bound_field.value() == 'John Doe'  # Initial value should be returned

    def test_value_bound(self):
        """Test value when the form is bound."""
        assert self.bound_field.value() == 'Jane Doe'  # Bound data should be returned

    def test_value_with_bound_data(self):
        """Test value with customized field definition."""
        class CustomField(forms.CharField):
            def bound_data(self, data, initial):
                return data.upper() if data else initial

        self.form.fields['name'] = CustomField(initial='John Doe')
        bound_field = BoundField(self.form, self.form.fields['name'], 'name')
        assert bound_field.value() == 'JANE DOE'  # Check transformation by custom bound_data

    def test_value_empty_data(self):
        """Test value with empty data and initial."""
        self.form = self.TestForm(data={})  # No input
        bound_field = BoundField(self.form, self.form.fields['name'], 'name')
        assert bound_field.value() == 'John Doe'  # Should still return initial