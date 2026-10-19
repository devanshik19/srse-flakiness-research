import pytest
from django.core.exceptions import ValidationError
from django.forms import Form, FormSet
from django.forms.fields import BooleanField, IntegerField
from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _

class TestForm(Form):
    field1 = IntegerField(required=True)
    field2 = BooleanField(required=False)

class TestFormSet(FormSet):
    form = TestForm

def test_full_clean_valid_data():
    formset = TestFormSet(data={
        'form-TOTAL_FORMS': '2',
        'form-0-field1': '1',
        'form-0-field2': 'True',
        'form-1-field1': '2',
        'form-1-field2': 'False',
    })
    formset.full_clean()

    assert formset.errors == [ErrorList([]), ErrorList([])]
    assert formset.non_form_errors == ErrorList([])

def test_full_clean_missing_management_form():
    formset = TestFormSet(data={})
    formset.full_clean()

    assert formset.non_form_errors[0].message == _('This field is required.')
    assert len(formset.errors) == 0  # No form errors because form data is empty

def test_full_clean_too_many_forms():
    formset = TestFormSet(data={
        'form-TOTAL_FORMS': '6',
        'form-0-field1': '1',
        'form-1-field1': '2',
        'form-2-field1': '3',
        'form-3-field1': '4',
        'form-4-field1': '5',
        'form-5-field1': '6',
    }, max_num=5)
    
    with pytest.raises(ValidationError) as exc_info:
        formset.full_clean()

    assert 'Please submit at most 5 forms.' in str(exc_info.value)

def test_full_clean_too_few_forms():
    formset = TestFormSet(data={
        'form-TOTAL_FORMS': '1',
        'form-0-field1': '',
    }, min_num=2)
    
    with pytest.raises(ValidationError) as exc_info:
        formset.full_clean()

    assert 'Please submit at least 2 forms.' in str(exc_info.value)

def test_full_clean_empty_forms():
    formset = TestFormSet(data={
        'form-TOTAL_FORMS': '3',
        'form-0-field1': '',
        'form-1-field1': '',
        'form-2-field1': '5',
    })
    formset.full_clean()

    assert len(formset.errors) == 3  # All forms should have errors
    assert formset.non_form_errors == ErrorList([])

def test_full_clean_with_deletions():
    formset = TestFormSet(data={
        'form-TOTAL_FORMS': '3',
        'form-0-id': '1',
        'form-0-field1': '5',
        'form-0-DELETE': 'on',
        'form-1-field1': '',
        'form-2-field1': '10',
    })
    formset.full_clean()

    assert formset.errors[0] == ErrorList([_('This field is required.')])  # Second form error
    assert formset.errors[1] == ErrorList([])  # Clean data for third form