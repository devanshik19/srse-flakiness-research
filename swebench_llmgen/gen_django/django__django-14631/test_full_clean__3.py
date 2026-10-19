import pytest
from django.core.exceptions import ValidationError
from django.forms import BaseForm
from django.utils.datastructures import MultiValueDict
from django.contrib.auth.models import User

class TestBaseForm(BaseForm):
    def __init__(self, data=None, error_class=None, empty_permitted=False):
        self.data = MultiValueDict(data or {})
        self._errors = None
        self.cleaned_data = None
        self.is_bound = bool(data)
        self.empty_permitted = empty_permitted
        self.changed_data = []

    def has_changed(self):
        return bool(self.changed_data)

    def _clean_fields(self):
        pass  # Simulate cleaning fields

    def _clean_form(self):
        pass  # Simulate cleaning form

    def _post_clean(self):
        pass  # Simulate post-clean actions


def test_full_clean_no_data():
    form = TestBaseForm()
    form.full_clean()
    assert form.cleaned_data is None
    assert len(form._errors) == 0


def test_full_clean_empty_permitted_no_changes():
    form = TestBaseForm(data={}, empty_permitted=True)
    form.full_clean()
    assert form.cleaned_data is None
    assert len(form._errors) == 0


def test_full_clean_empty_permitted_with_changes():
    form = TestBaseForm(data={}, empty_permitted=True)
    form.changed_data = ['some_change']
    form.full_clean()
    assert form.cleaned_data is None
    assert len(form._errors) == 0


def test_full_clean_not_empty_permitted():
    form = TestBaseForm(data={}, empty_permitted=False)
    form.full_clean()
    assert len(form._errors) == 0  # Assuming _clean_fields adds errors
    assert form.cleaned_data is None  # Needs actual clean logic to change this