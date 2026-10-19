import pytest
from django.contrib.auth.models import User
from django.forms import BaseForm

class TestBaseForm(BaseForm):
    def __init__(self, data=None, files=None):
        self.is_bound = bool(data) or bool(files)
        self._errors = None
        self.fields = ['field1', 'field2']  # example fields for testing

@pytest.fixture
def bound_form():
    data = {'field1': 'value1'}
    return TestBaseForm(data=data)

@pytest.fixture
def unbound_form():
    return TestBaseForm()

def test_repr_bound_with_no_errors(bound_form):
    assert repr(bound_form) == '<TestBaseForm bound=True, valid=True, fields=(field1;field2)>'

def test_repr_bound_with_errors(bound_form):
    bound_form._errors = {NON_FIELD_ERRORS: ["This is an error."]}
    assert repr(bound_form) == '<TestBaseForm bound=True, valid=False, fields=(field1;field2)>'

def test_repr_unbound_with_unknown_status(unbound_form):
    assert repr(unbound_form) == '<TestBaseForm bound=False, valid=Unknown, fields=(field1;field2)>'

def test_repr_unbound_with_errors(unbound_form):
    unbound_form._errors = {NON_FIELD_ERRORS: ["This is an error."]}
    assert repr(unbound_form) == '<TestBaseForm bound=False, valid=Unknown, fields=(field1;field2)>'