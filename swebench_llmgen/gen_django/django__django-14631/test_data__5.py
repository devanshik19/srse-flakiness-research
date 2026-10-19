import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField

class TestForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()

@pytest.fixture
def bound_field():
    form = TestForm(data={'username': 'testuser', 'email': 'test@example.com'})
    form.is_valid()
    field = form.fields['username']
    name = field.label if field.label else 'username'
    return BoundField(form, field, name)

def test_data_with_valid_input(bound_field):
    assert bound_field.data == 'testuser'

def test_data_with_no_input():
    form = TestForm(data={})
    form.is_valid()
    field = form.fields['username']
    name = field.label if field.label else 'username'
    bound_field = BoundField(form, field, name)
    assert bound_field.data is None