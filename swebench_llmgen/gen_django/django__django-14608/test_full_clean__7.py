import pytest
from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms.fields import BooleanField, IntegerField
from django.forms.utils import ErrorList
from django.forms.formsets import BaseFormSet
from django.utils.translation import ngettext

class TestForm(Form):
    field_a = IntegerField()
    field_b = BooleanField()

@pytest.fixture
def formset():
    return BaseFormSet(data={'form-0-field_a': '1', 'form-0-field_b': 'True', 
                              'form-1-field_a': '', 'form-1-field_b': ''},
                       files=None, auto_id='id_%s', prefix='form', 
                       initial=[], error_class=ErrorList, 
                       error_messages={})

def test_full_clean_valid(formset):
    formset.is_bound = True
    formset.forms = [TestForm(data={'field_a': '1', 'field_b': 'True'}),
                     TestForm(data={'field_a': '', 'field_b': ''})]
    
    formset.full_clean()
    
    assert not formset.errors
    assert len(formset._non_form_errors) == 0

def test_full_clean_missing_management_form(formset):
    formset.is_bound = True
    formset.management_form = TestForm(data={})
    formset.forms = [TestForm(data={}), TestForm(data={})]
    
    formset.full_clean()
    
    assert len(formset._non_form_errors) == 1
    assert isinstance(formset._non_form_errors[0], ValidationError)

def test_full_clean_too_many_forms(formset):
    formset.is_bound = True
    formset.management_form = TestForm(data={})
    formset.max_num = 1
    formset.forms = [TestForm(data={'field_a': '1'}), 
                     TestForm(data={'field_a': '2'})]
    
    with pytest.raises(ValidationError):
        formset.full_clean()

def test_full_clean_too_few_forms(formset):
    formset.is_bound = True
    formset.management_form = TestForm(data={})
    formset.min_num = 2
    formset.forms = [TestForm(data={'field_a': '1'})]
    
    with pytest.raises(ValidationError):
        formset.full_clean()