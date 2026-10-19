import pytest
from django.forms import BaseForm
from django.contrib.auth.models import User


class TestBaseForm(BaseForm):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None,
                 error_class=ErrorList, label_suffix=None, empty_permitted=False,
                 field_order=None, use_required_attribute=None, renderer=None):
        self.data = data or {}
        self.files = files or {}
        self.is_bound = bool(data) or bool(files)
        self.fields = ['first_name', 'last_name', 'email']
        self._errors = None

    def is_valid(self):
        return self._errors is None and self.is_bound


def test_repr_no_errors():
    form = TestBaseForm(data={'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@example.com'})
    form._errors = None  # Simulating a case where there are no errors
    expected_repr = '<TestBaseForm bound=True, valid=Unknown, fields=(first_name;last_name;email)>'
    assert repr(form) == expected_repr


def test_repr_with_errors():
    form = TestBaseForm(data={'first_name': 'John', 'last_name': '', 'email': 'john.doe@example.com'})
    form._errors = {'last_name': 'This field is required.'}  # Simulating validation error
    expected_repr = '<TestBaseForm bound=True, valid=False, fields=(first_name;last_name;email)>'
    assert repr(form) == expected_repr


def test_repr_not_bound():
    form = TestBaseForm()  # No data or files, simulating unbound form
    form._errors = None  # No errors even though it's unbound
    expected_repr = '<TestBaseForm bound=False, valid=Unknown, fields=(first_name;last_name;email)>'
    assert repr(form) == expected_repr