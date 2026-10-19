import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField

class TestBoundFieldValue:
    class TestForm(forms.Form):
        username = forms.CharField(initial='testuser')

    @pytest.fixture
    def form_with_data(self):
        return self.TestForm(data={'username': 'newuser'})

    @pytest.fixture
    def bound_field(self, form_with_data):
        field = self.TestForm.base_fields['username']
        return BoundField(form_with_data, field, 'username')

    @pytest.fixture
    def bound_field_initial(self, form_with_data):
        form_with_data.is_bound = False
        field = self.TestForm.base_fields['username']
        return BoundField(form_with_data, field, 'username')

    def test_value_with_bound_data(self, bound_field):
        assert bound_field.value() == 'newuser'

    def test_value_without_bound_data(self, bound_field_initial):
        assert bound_field_initial.value() == 'testuser'