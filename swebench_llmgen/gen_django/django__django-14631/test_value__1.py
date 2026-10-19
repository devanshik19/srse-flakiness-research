import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField

class TestBoundField:
    @pytest.fixture
    def setup_form(self):
        class TestForm(forms.Form):
            username = forms.CharField(initial='testuser')
        
        form = TestForm(data={'username': 'newuser'})
        return form

    def test_value_with_bound_form(self, setup_form):
        field = setup_form['username']
        bound_field = BoundField(setup_form, field.field, 'username')
        assert bound_field.value() == 'newuser'

    def test_value_with_unbound_form(self):
        class TestForm(forms.Form):
            username = forms.CharField(initial='testuser')
        
        form = TestForm()
        field = form['username']
        bound_field = BoundField(form, field.field, 'username')
        assert bound_field.value() == 'testuser'

    def test_value_with_initial_and_no_data(self):
        class TestForm(forms.Form):
            username = forms.CharField(initial='testuser')
        
        form = TestForm()  # unbound form
        field = form['username']
        bound_field = BoundField(form, field.field, 'username')
        bound_field.data = None  # Simulating no data being provided
        assert bound_field.value() == 'testuser'

    def test_value_with_initial_and_bound_data(self, setup_form):
        field = setup_form['username']
        bound_field = BoundField(setup_form, field.field, 'username')
        bound_field.data = 'changeduser'  # Simulating data being provided
        assert bound_field.value() == 'changeduser'