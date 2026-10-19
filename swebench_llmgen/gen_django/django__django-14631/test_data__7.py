import pytest
from django.forms import BoundField
from django import forms
from django.contrib.auth.models import User

class TestForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()

def test_bound_field_data():
    user = User.objects.create_user('testuser', 'test@example.com', 'password123')
    
    form = TestForm(data={'username': 'testuser', 'email': 'test@example.com'})
    form.is_bound = True  # Simulating bound form state
    bound_field_username = BoundField(form, form.fields['username'], 'username')
    bound_field_email = BoundField(form, form.fields['email'], 'email')

    assert bound_field_username.data() == 'testuser'
    assert bound_field_email.data() == 'test@example.com'

    # Test when the field data is not provided
    empty_form = TestForm(data={})
    empty_form.is_bound = True  # Simulating bound form state
    bound_field_username_empty = BoundField(empty_form, empty_form.fields['username'], 'username')

    assert bound_field_username_empty.data() is None