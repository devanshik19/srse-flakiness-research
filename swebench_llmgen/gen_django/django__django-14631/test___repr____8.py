import pytest
from django.forms import BaseForm
from django.contrib.auth.models import User

class TestBaseForm(BaseForm):
    def __init__(self, data=None):
        super().__init__(data, None, None, None, None, None, None, None, None, None, None, None)
        self.fields = ['field1', 'field2']
        self.is_bound = bool(data)
        self._errors = None

def test_repr_no_errors():
    form = TestBaseForm(data={'field1': 'value1', 'field2': 'value2'})
    assert repr(form) == '<TestBaseForm bound=True, valid=True, fields=(field1;field2)>'

def test_repr_with_errors():
    form = TestBaseForm(data={'field1': 'value1', 'field2': 'value2'})
    form._errors = {'field1': [ValidationError("Invalid")]}

    assert repr(form) == '<TestBaseForm bound=True, valid=False, fields=(field1;field2)>'

def test_repr_unknown_state():
    form = TestBaseForm()
    form._errors = None

    assert repr(form) == '<TestBaseForm bound=False, valid=Unknown, fields=(field1;field2)>'