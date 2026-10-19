import pytest
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms.utils import ErrorDict

class TestBaseForm(forms.BaseForm):
    
    def __init__(self, *args, **kwargs):
        self.data = kwargs.pop('data', None)
        self.is_bound = self.data is not None
        self.empty_permitted = kwargs.pop('empty_permitted', False)
        self.cleaned_data = {}
        self._errors = ErrorDict()
        super().__init__(*args, **kwargs)

    def has_changed(self):
        return bool(self.data)

    def _clean_fields(self):
        for field_name in self.fields:
            value = self.data.get(field_name)
            if value is None:
                raise ValidationError(f"{field_name} cannot be None.")
            self.cleaned_data[field_name] = value

    def _clean_form(self):
        pass

    def _post_clean(self):
        pass


def test_full_clean_valid_data():
    form_data = {'username': 'testuser'}
    form = TestBaseForm(data=form_data)
    form.fields = ['username']
    
    form.full_clean()
    
    assert not form.errors  # Expecting no errors
    assert form.cleaned_data == form_data  # Expecting cleaned data to match input


def test_full_clean_empty_data_permitted():
    form_data = {}
    form = TestBaseForm(data=form_data, empty_permitted=True)
    form.fields = ['username']
    
    form.full_clean()
    
    assert not form.errors  # Expecting no errors
    assert form.cleaned_data == {}  # Expecting cleaned data to be empty


def test_full_clean_empty_data_not_permitted():
    form_data = {}
    form = TestBaseForm(data=form_data, empty_permitted=False)
    form.fields = ['username']
    
    with pytest.raises(ValidationError):
        form.full_clean()  # Should raise validation error


def test_full_clean_has_changed():
    form_data = {'username': 'testuser'}
    form = TestBaseForm(data=form_data)
    form.fields = ['username']
    
    form.full_clean()
    
    assert form.cleaned_data['username'] == 'testuser'


def test_full_clean_no_initial_change():
    form_data = {'username': 'testuser'}
    form = TestBaseForm(data=form_data, empty_permitted=True)
    form.fields = ['username']
    
    # Simulating no change
    form.has_changed = lambda: False
    form.full_clean()
    
    assert not form.errors  # Expecting no errors
    assert form.cleaned_data == {}  # Expecting cleaned data to be empty