import copy
import pytest
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.forms import BaseForm, Field, ErrorDict, ErrorList

class TestBaseForm(BaseForm):
    def __init__(self, data=None, files=None, **kwargs):
        self.is_bound = bool(data) or bool(files)
        self.data = data or {}
        self.files = files or {}
        super().__init__(data, files, **kwargs)
        self.cleaned_data = {}
        self._errors = ErrorDict()

    def has_changed(self):
        return True

    def _clean_fields(self):
        pass

    def _clean_form(self):
        pass

    def _post_clean(self):
        pass


def test_full_clean_empty_data():
    form = TestBaseForm(data={})
    form.full_clean()
    assert form._errors == {}
    assert form.cleaned_data == {}


def test_full_clean_with_changed_data():
    form = TestBaseForm(data={'field1': 'value1'})
    form.full_clean()
    assert isinstance(form._errors, ErrorDict)


def test_full_clean_not_bound():
    form = TestBaseForm(data=None)
    form.full_clean()
    assert form._errors == {}
    assert form.cleaned_data == {}


def test_full_clean_with_empty_permitted_and_no_change():
    form = TestBaseForm(data={}, empty_permitted=True)
    form.full_clean()
    assert form._errors == {}
    assert form.cleaned_data == {}


def test_full_clean_with_empty_permitted_and_change():
    form = TestBaseForm(data={'field1': 'value1'}, empty_permitted=True)
    form.full_clean()
    assert isinstance(form._errors, ErrorDict)