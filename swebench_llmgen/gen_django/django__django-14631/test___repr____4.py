import pytest
from django import forms

class TestBaseForm:

    def test_repr_unbound_without_errors(self):
        form = forms.BaseForm()
        form.is_bound = False
        form._errors = None
        expected_repr = '<BaseForm bound=False, valid=Unknown, fields=()>'
        assert repr(form) == expected_repr

    def test_repr_bound_with_no_errors(self):
        form = forms.BaseForm()
        form.is_bound = True
        form._errors = {}
        form.fields = {'field1': forms.Field(), 'field2': forms.Field()}
        expected_repr = '<BaseForm bound=True, valid=True, fields=(field1;field2)>'
        assert repr(form) == expected_repr

    def test_repr_bound_with_errors(self):
        form = forms.BaseForm()
        form.is_bound = True
        form._errors = {'field1': forms.ErrorList(['Error message'])}
        form.fields = {'field1': forms.Field(), 'field2': forms.Field()}
        expected_repr = '<BaseForm bound=True, valid=False, fields=(field1;field2)>'
        assert repr(form) == expected_repr

    def test_repr_empty_fields(self):
        form = forms.BaseForm()
        form.is_bound = True
        form._errors = {}
        form.fields = {}
        expected_repr = '<BaseForm bound=True, valid=True, fields=()>'
        assert repr(form) == expected_repr