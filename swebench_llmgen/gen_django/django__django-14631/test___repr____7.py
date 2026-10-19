import pytest
from django.contrib.auth.models import User
from django.forms import BaseForm

class TestBaseForm(BaseForm):
    def __init__(self, data=None, files=None):
        self.data = data or {}
        self.files = files or {}
        self.is_bound = bool(data or files)
        self.fields = ['field1', 'field2']
        self._errors = None

    def is_valid(self):
        return not self._errors

def test_repr_valid():
    form = TestBaseForm(data={'field1': 'value1', 'field2': 'value2'})
    form._errors = {}
    expected_repr = '<TestBaseForm bound=True, valid=True, fields=(field1;field2)>'
    assert repr(form) == expected_repr

def test_repr_invalid():
    form = TestBaseForm(data={'field1': 'value1', 'field2': 'value2'})
    form._errors = {'field1': [ValidationError('Error message')]}
    expected_repr = '<TestBaseForm bound=True, valid=False, fields=(field1;field2)>'
    assert repr(form) == expected_repr

def test_repr_unknown():
    form = TestBaseForm()
    form._errors = None
    expected_repr = '<TestBaseForm bound=False, valid=Unknown, fields=(field1;field2)>'
    assert repr(form) == expected_repr