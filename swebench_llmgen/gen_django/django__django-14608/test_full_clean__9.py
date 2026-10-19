import pytest
from django.core.exceptions import ValidationError
from django.forms import Form, BaseFormSet
from django.forms.fields import BooleanField, IntegerField
from django.forms.utils import ErrorList
from django.utils.translation import ngettext

class TestForm(Form):
    integer_field = IntegerField(required=True)
    boolean_field = BooleanField(required=False)

class TestFormSet(BaseFormSet):
    def clean(self):
        if len(self.forms) < 2:
            raise ValidationError("At least two forms are required.")

def test_full_clean_valid_forms():
    formset = TestFormSet(data={
        'form-0-integer_field': '1',
        'form-0-boolean_field': 'on',
        'form-1-integer_field': '2',
        'form-1-boolean_field': 'off',
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '10',
    })
    formset.full_clean()
    assert not formset.errors
    assert isinstance(formset._non_form_errors, ErrorList)
    assert not formset._non_form_errors

def test_full_clean_missing_management_form():
    formset = TestFormSet(data={
        'form-0-integer_field': '1',
        'form-0-boolean_field': 'on',
        'form-TOTAL_FORMS': '1',
    })
    formset.full_clean()
    assert formset._non_form_errors
    assert isinstance(formset._non_form_errors[0], ValidationError)

def test_full_clean_too_many_forms():
    formset = TestFormSet(data={
        'form-0-integer_field': '1',
        'form-0-boolean_field': 'on',
        'form-1-integer_field': '2',
        'form-1-boolean_field': 'off',
        'form-2-integer_field': '3',
        'form-TOTAL_FORMS': '3',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '2',
    })
    with pytest.raises(ValidationError):
        formset.full_clean()

def test_full_clean_too_few_forms():
    formset = TestFormSet(data={
        'form-0-integer_field': '1',
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MIN_NUM_FORMS': '2',
    })
    with pytest.raises(ValidationError):
        formset.full_clean()

def test_full_clean_no_changed_forms():
    formset = TestFormSet(data={
        'form-0-integer_field': '1',
        'form-0-boolean_field': 'on',
        'form-1-integer_field': '1',
        'form-1-boolean_field': 'on',
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '2',
    })
    formset.full_clean()
    assert len(formset._errors) == 0

def test_full_clean_with_deletion():
    data = {
        'form-0-integer_field': '1',
        'form-0-boolean_field': 'on',
        'form-1-integer_field': '',
        'form-1-DELETE': 'on',
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '2',
    }
    formset = TestFormSet(data=data)
    formset.full_clean()
    assert len(formset._errors) == 1  # The first form is valid, second is deleted.

    assert not formset._non_form_errors