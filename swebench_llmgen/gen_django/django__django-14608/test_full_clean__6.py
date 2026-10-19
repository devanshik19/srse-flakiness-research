import pytest
from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms.fields import BooleanField, IntegerField
from django.forms.utils import ErrorList
from django.forms.widgets import HiddenInput, NumberInput
from django.utils.translation import gettext_lazy as _, ngettext
from django.forms import BaseFormSet

class TestForm(Form):
    boolean_field = BooleanField(required=False)
    integer_field = IntegerField(required=True)

class TestFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.forms = [TestForm(data) for data in args[0]]

def test_full_clean_valid():
    data = [
        {'boolean_field': True, 'integer_field': 1},
        {'boolean_field': False, 'integer_field': 2}
    ]
    formset = TestFormSet(data)
    
    formset.full_clean()
    
    assert not formset.errors  # Check that there are no form errors
    assert not formset.non_form_errors  # Check that there are no non-form errors

def test_full_clean_missing_management_form():
    data = [
        {'boolean_field': True, 'integer_field': 1},
    ]
    formset = TestFormSet(data)
    formset.management_form = TestForm()  # Simulating invalid management form
    
    formset.full_clean()
    
    assert len(formset.non_form_errors) == 1  # Check that there is a non-form error
    assert "missing_management_form" in str(formset.non_form_errors[0])  # Error type

def test_full_clean_too_many_forms():
    data = [
        {'boolean_field': True, 'integer_field': 1},
        {'boolean_field': False, 'integer_field': 2},
        {'boolean_field': True, 'integer_field': 3},  # Excess form
    ]
    formset = TestFormSet(data)
    formset.max_num = 2  # Setting max number of forms
    formset.full_clean()
    
    assert len(formset.non_form_errors) == 1  # Check that there is a non-form error
    assert "Please submit at most" in str(formset.non_form_errors[0])  # Error message

def test_full_clean_too_few_forms():
    data = [
        {'boolean_field': True, 'integer_field': 1},
    ]
    formset = TestFormSet(data)
    formset.min_num = 2  # Setting min number of forms
    formset.full_clean()
    
    assert len(formset.non_form_errors) == 1  # Check that there is a non-form error
    assert "Please submit at least" in str(formset.non_form_errors[0])  # Error message

def test_full_clean_with_empty_form():
    data = [
        {'boolean_field': True, 'integer_field': 1},
        {},  # Empty form
    ]
    formset = TestFormSet(data)
    formset.full_clean()

    assert len(formset.errors) == 1  # Check that there is an error for the empty form
    assert formset.errors[1]['integer_field']  # Check specific field has error