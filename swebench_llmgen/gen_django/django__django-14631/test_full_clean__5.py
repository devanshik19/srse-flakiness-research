import pytest
from django.forms import BaseForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms.fields import CharField

class TestForm(BaseForm):
    username = CharField(required=True)
    password = CharField(required=True)

@pytest.mark.parametrize("data, expected_errors", [
    ({}, {'username': ['This field is required.'], 'password': ['This field is required.']}),
    ({'username': 'user1', 'password': 'testpass'}, {}),
    ({'username': 'user2'}, {'password': ['This field is required.']}),
])
def test_full_clean(data, expected_errors):
    form = TestForm(data=data, files=None, auto_id=None, prefix=None, initial=None,
                    error_class=None, label_suffix=None, empty_permitted=False, 
                    field_order=None, use_required_attribute=None, renderer=None)
    form.full_clean()
    
    if expected_errors:
        assert form.errors == expected_errors
    else:
        assert not form.errors
        assert form.cleaned_data['username'] == data.get('username')
        assert form.cleaned_data['password'] == data.get('password')

def test_full_clean_when_not_bound():
    form = TestForm(data=None, files=None, auto_id=None, prefix=None, initial=None,
                    error_class=None, label_suffix=None, empty_permitted=False,
                    field_order=None, use_required_attribute=None, renderer=None)
    form.full_clean()
    assert not form.errors
    assert not form.cleaned_data