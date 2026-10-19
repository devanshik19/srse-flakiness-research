import pytest
from django.core.exceptions import ValidationError
from django.forms import Form, BaseFormSet
from django.forms.fields import BooleanField, IntegerField
from django.forms.utils import ErrorList

class TestForm(Form):
    number = IntegerField(required=True)
    active = BooleanField(required=False)

class TestFormSet(BaseFormSet):
    form = TestForm

def test_full_clean_valid_forms():
    formset = TestFormSet(data={
        'form-0-number': '1',
        'form-0-active': 'on',
        'form-1-number': '2',
        'form-1-active': '',
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '0',
    })
    formset.full_clean()

    assert not formset.errors
    assert not formset.non_form_errors

def test_full_clean_missing_management_form():
    formset = TestFormSet(data={
        'form-0-number': '1',
        'form-0-active': 'on',
        'form-TOTAL_FORMS': '1',
    })
    formset.full_clean()

    assert formset.non_form_errors
    assert len(formset.non_form_errors) == 1

def test_full_clean_too_many_forms():
    formset = TestFormSet(data={
        'form-0-number': '1',
        'form-TOTAL_FORMS': '4',
        'form-INITIAL_FORMS': '0',
    })
    formset.max_num = 2
    formset.full_clean()

    assert formset.non_form_errors
    assert len(formset.non_form_errors) == 1

def test_full_clean_too_few_forms():
    formset = TestFormSet(data={
        'form-0-number': '1',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
    })
    formset.min_num = 2
    formset.full_clean()

    assert formset.non_form_errors
    assert len(formset.non_form_errors) == 1

def test_full_clean_empty_form():
    formset = TestFormSet(data={
        'form-0-number': '',
        'form-0-active': 'on',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
    })
    formset.full_clean()

    assert formset.errors[0]['number']
    assert len(formset.errors) == 1