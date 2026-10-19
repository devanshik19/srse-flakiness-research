import pytest
from django.contrib.auth.models import User
from django.forms import BaseForm

class TestBaseForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = ['field1', 'field2']
        self._errors = None
    
    @property
    def is_bound(self):
        return bool(self.data)

def test_repr_valid():
    form_data = {'field1': 'value1', 'field2': 'value2'}
    form = TestBaseForm(data=form_data)
    form._errors = {}
    
    expected_repr = '<TestBaseForm bound=False, valid=True, fields=(field1;field2)>'
    assert repr(form) == expected_repr

def test_repr_with_errors():
    form_data = {'field1': 'value1', 'field2': 'value2'}
    form = TestBaseForm(data=form_data)
    form._errors = {'field1': ['This field is required.']}
    
    expected_repr = '<TestBaseForm bound=False, valid=False, fields=(field1;field2)>'
    assert repr(form) == expected_repr

def test_repr_unknown_errors():
    form = TestBaseForm(data={})
    form._errors = None
    
    expected_repr = '<TestBaseForm bound=False, valid=Unknown, fields=(field1;field2)>'
    assert repr(form) == expected_repr

def test_repr_bound():
    form_data = {'field1': 'value1', 'field2': 'value2'}
    form = TestBaseForm(data=form_data)
    form.is_bound = True
    form._errors = {}
    
    expected_repr = '<TestBaseForm bound=True, valid=True, fields=(field1;field2)>'
    assert repr(form) == expected_repr