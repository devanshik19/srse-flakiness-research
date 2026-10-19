import pytest
from django.forms import Form, FormSet
from django.core.exceptions import ValidationError
from django.forms.fields import IntegerField, BooleanField


class TestForm(Form):
    number = IntegerField(required=True)
    is_active = BooleanField(required=False)


class TestFormSet(FormSet):
    form_class = TestForm
    validate_max = True
    max_num = 3
    min_num = 1
    validate_min = True

    
def test_full_clean_valid_forms():
    form_data = [{'number': 1, 'is_active': True}, {'number': 2}, {'number': 3}]
    formset = TestFormSet(data={'form-0-number': 1, 'form-0-is_active': True,
                                 'form-1-number': 2,
                                 'form-2-number': 3,
                                 'form-TOTAL_FORMS': 3})
    
    assert formset.is_valid()
    
    formset.full_clean()
    
    assert formset._errors == []
    assert formset._non_form_errors == []


def test_full_clean_missing_management_form():
    form_data = [{'number': 1}]
    formset = TestFormSet(data={'form-0-number': 1, 'form-TOTAL_FORMS': 1})

    assert not formset.management_form.is_valid()

    formset.full_clean()

    assert len(formset._non_form_errors) == 1
    assert 'missing_management_form' in str(formset._non_form_errors[0])


def test_full_clean_too_many_forms():
    formset = TestFormSet(data={'form-0-number': 1, 'form-TOTAL_FORMS': 4})

    formset.full_clean()

    assert len(formset._non_form_errors) == 1
    assert 'too_many_forms' in str(formset._non_form_errors)


def test_full_clean_too_few_forms():
    formset = TestFormSet(data={'form-0-number': 1, 'form-TOTAL_FORMS': 0})

    formset.full_clean()

    assert len(formset._non_form_errors) == 1
    assert 'too_few_forms' in str(formset._non_form_errors)