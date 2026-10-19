import pytest
from django.core.exceptions import ValidationError
from django.forms import BaseForm
from django.contrib.auth.models import User

class TestBaseForm(BaseForm):
    def __init__(self, data=None, files=None, initial=None, empty_permitted=False):
        self.data = data or {}
        self.files = files or {}
        self.initial = initial or {}
        self.is_bound = bool(data) or bool(files)
        self.empty_permitted = empty_permitted
        self.cleaned_data = {}
        self._errors = None

    def has_changed(self):
        return self.data != self.initial

    def _clean_fields(self):
        # Example field cleaning logic (would need real implementation)
        if 'username' in self.data:
            self.cleaned_data['username'] = self.data['username']
        else:
            self.add_error('username', 'This field is required.')

    def _clean_form(self):
        pass

    def _post_clean(self):
        pass

    def add_error(self, field, error):
        if self._errors is None:
            self._errors = ErrorDict()
        if field not in self._errors:
            self._errors[field] = ErrorList()
        self._errors[field].append(error)

def test_full_clean_with_bound_data_and_no_changes():
    form_data = {'username': 'testuser'}
    form = TestBaseForm(data=form_data, initial=form_data, empty_permitted=True)
    form.full_clean()
    
    assert form.cleaned_data['username'] == 'testuser'
    assert form._errors is None

def test_full_clean_with_bound_data_and_changes():
    form_data = {'username': 'newuser'}
    initial_data = {'username': 'olduser'}

    form = TestBaseForm(data=form_data, initial=initial_data, empty_permitted=False)
    form.full_clean()

    assert form.cleaned_data['username'] == 'newuser'
    assert form.errors['username'] is None

def test_full_clean_with_missing_required_field():
    form_data = {}
    form = TestBaseForm(data=form_data, initial={}, empty_permitted=False)
    form.full_clean()

    assert 'username' in form.errors
    assert form.errors['username'] == ['This field is required.']

def test_full_clean_with_empty_permitted_and_no_changes():
    form_data = {}
    form = TestBaseForm(data=form_data, initial=form_data, empty_permitted=True)
    form.full_clean()

    assert form.cleaned_data == {}
    assert form._errors is None