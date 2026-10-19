import pytest
from django.core.exceptions import ValidationError
from django.forms import BaseForm
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDict

class TestBaseForm(BaseForm):
    def __init__(self, data=None, *args, **kwargs):
        self.is_bound = data is not None
        self.cleaned_data = {}
        self.empty_permitted = kwargs.get('empty_permitted', True)
        super().__init__(data=data, *args, **kwargs)

    def has_changed(self):
        return self.data != self.initial

    def _clean_fields(self):
        pass

    def _clean_form(self):
        pass

    def _post_clean(self):
        pass

def test_full_clean_with_bound_data():
    form_data = {'username': 'testuser', 'password': 'testpass'}
    form = TestBaseForm(data=form_data)
    form.full_clean()
    assert not form._errors
    assert form.cleaned_data == {}

def test_full_clean_with_empty_permitted_and_no_changes():
    form_data = {'username': 'testuser', 'password': 'testpass'}
    initial_data = form_data.copy()
    form = TestBaseForm(data=form_data, initial=initial_data, empty_permitted=True)
    form.full_clean()
    assert not form._errors
    assert form.cleaned_data == {}

def test_full_clean_with_empty_permitted_and_changes():
    form_data = {'username': 'changeduser', 'password': 'testpass'}
    initial_data = {'username': 'testuser', 'password': 'testpass'}
    form = TestBaseForm(data=form_data, initial=initial_data, empty_permitted=True)
    
    # These will be empty since _clean_fields is a placeholder
    form.full_clean()  
    assert not form._errors
    assert form.cleaned_data == {}

def test_full_clean_with_not_bound_form():
    form = TestBaseForm(data=None)
    form.full_clean()
    assert not form._errors
    assert form.cleaned_data == {}