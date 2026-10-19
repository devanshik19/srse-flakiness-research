import pytest
from django import forms
from django.contrib.auth.models import User

class TestBaseForm(forms.BaseForm):
    def __init__(self, data=None):
        self.is_bound = bool(data)
        self._errors = None
        self.fields = ['username', 'password']
        super().__init__(data=data, files=None, auto_id=None, prefix=None, initial=None, 
                         error_class=forms.ErrorList, label_suffix=None, 
                         empty_permitted=False, field_order=None, 
                         use_required_attribute=True, renderer=None)

def test_repr_with_errors():
    form = TestBaseForm(data={'username': 'testuser', 'password': 'testpass'})
    form._errors = {'username': ['This field is required.']}
    expected_repr = '<TestBaseForm bound=True, valid=False, fields=(username;password)>'
    assert repr(form) == expected_repr

def test_repr_without_errors():
    form = TestBaseForm(data={'username': 'testuser', 'password': 'testpass'})
    form._errors = {}
    expected_repr = '<TestBaseForm bound=True, valid=True, fields=(username;password)>'
    assert repr(form) == expected_repr

def test_repr_unbound():
    form = TestBaseForm(data=None)
    form._errors = None
    expected_repr = '<TestBaseForm bound=False, valid=Unknown, fields=(username;password)>'
    assert repr(form) == expected_repr