import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms import BoundField


class TestForm(forms.Form):
    username = forms.CharField()


@pytest.fixture
def bound_field():
    form = TestForm(data={'username': 'test_user'})
    form.is_valid()
    field = form.fields['username']
    name = 'username'
    return BoundField(form, field, name)


def test_bound_field_data_with_value(bound_field):
    assert bound_field.data == 'test_user'


def test_bound_field_data_with_no_value():
    form = TestForm(data={})
    form.is_valid()
    field = form.fields['username']
    name = 'username'
    bound_field = BoundField(form, field, name)
    assert bound_field.data is None