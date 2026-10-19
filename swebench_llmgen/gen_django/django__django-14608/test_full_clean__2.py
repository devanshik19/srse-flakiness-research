import pytest
from django.core.exceptions import ValidationError
from django.forms import Form, CharField, IntegerField
from django.forms.formsets import BaseFormSet
from django.forms.utils import ErrorList
from django.forms.widgets import HiddenInput

class TestForm(Form):
    name = CharField(required=True)
    age = IntegerField(required=True)

class TestFormSet(BaseFormSet):
    form = TestForm

@pytest.fixture
def formset_with_valid_data():
    data = {'form-0-name': 'Alice', 'form-0-age': 30,
            'form-1-name': 'Bob', 'form-1-age': 25,
            'form-TOTAL_FORMS': 2}
    formset = TestFormSet(data=data)
    return formset

@pytest.fixture
def formset_with_invalid_data():
    data = {'form-0-name': 'Alice', 'form-0-age': '',  # Invalid: age is required
            'form-1-name': '',  # Invalid: name is required
            'form-TOTAL_FORMS': 2}
    formset = TestFormSet(data=data)
    return formset

@pytest.fixture
def formset_with_missing_management_form():
    data = {'form-0-name': 'Alice', 'form-0-age': 30}
    formset = TestFormSet(data=data)
    return formset

def test_full_clean_valid(formset_with_valid_data):
    formset = formset_with_valid_data
    formset.full_clean()
    assert not formset.errors
    assert not formset.non_form_errors

def test_full_clean_invalid(formset_with_invalid_data):
    formset = formset_with_invalid_data
    formset.full_clean()
    assert formset.errors[0][0]  # First form has errors
    assert formset.errors[1][0]  # Second form has errors
    assert len(formset.non_form_errors) == 0

def test_full_clean_missing_management_form(formset_with_missing_management_form):
    formset = formset_with_missing_management_form
    formset.full_clean()
    assert len(formset.non_form_errors) == 1
    assert isinstance(formset.non_form_errors[0], ValidationError)
    assert formset.non_form_errors[0].code == 'missing_management_form'