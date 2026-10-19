import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField

class TestForm(forms.Form):
    username = forms.CharField(initial='test_user')

@pytest.fixture
def bound_field():
    form = TestForm(data={'username': 'test_user'})
    form.is_bound = True
    field = form.fields['username']
    return BoundField(form, field, 'username')

def test_value_initial(bound_field):
    # Ensure the value returns the initial value when form is not bound
    bound_field.form.is_bound = False
    assert bound_field.value() == 'test_user'

def test_value_bound_data(bound_field):
    # Ensure the value returns correct bound data when form is bound
    user_instance = User.objects.create(username='test_user')
    bound_field.data = 'new_value'
    bound_field.initial = user_instance.username
    bound_field.form.is_bound = True

    def mock_bound_data(data, initial):
        return data if data else initial

    bound_field.field.bound_data = mock_bound_data
    assert bound_field.value() == 'new_value'
    
def test_value_prepare_value(bound_field):
    # Ensure that prepare_value correctly processes the data
    bound_field.data = 'test_user'
    bound_field.form.is_bound = True
    
    def mock_prepare_value(data):
        return f"Processed: {data}"

    bound_field.field.prepare_value = mock_prepare_value
    assert bound_field.value() == "Processed: new_value"