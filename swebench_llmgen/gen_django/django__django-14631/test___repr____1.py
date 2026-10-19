import pytest
from django.contrib.auth.models import User
from django.forms import BaseForm

class TestBaseForm(BaseForm):
    def __init__(self, data=None, files=None, auto_id=None, prefix=None, initial=None,
                 error_class=None, label_suffix=None, empty_permitted=False, field_order=None,
                 use_required_attribute=None, renderer=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class,
                         label_suffix, empty_permitted, field_order, use_required_attribute, renderer)
        self.is_bound = bool(data)
        self._errors = None
        self.fields = ['field1', 'field2', 'field3']

def test_repr_bound_valid():
    form = TestBaseForm(data={'field1': 'value1', 'field2': 'value2'})
    assert repr(form) == '<TestBaseForm bound=True, valid=True, fields=(field1;field2;field3)>'

def test_repr_bound_invalid():
    form = TestBaseForm(data={'field1': 'value1'}, files={'field2': 'invalid_file'})
    form._errors = {'field1': [ValidationError("This field is required.")]}
    assert repr(form) == '<TestBaseForm bound=True, valid=False, fields=(field1;field2;field3)>'

def test_repr_not_bound():
    form = TestBaseForm()
    assert repr(form) == '<TestBaseForm bound=False, valid=Unknown, fields=(field1;field2;field3)>'