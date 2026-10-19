import pytest
from django.core.exceptions import ValidationError
from django.forms import Form, FormSet
from django.forms.fields import BooleanField, IntegerField
from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _

class SampleForm(Form):
    integer_field = IntegerField(required=True)
    boolean_field = BooleanField(required=False)

class TestBaseFormSet:
    @pytest.fixture
    def formset(self):
        return FormSet(form=SampleForm, data={}, auto_id='id_%s', prefix='sample')

    def test_full_clean_invalid_management_form(self, formset):
        formset.data = {'form-0-integer_field': '1', 'form-1-integer_field': ''}
        formset.full_clean()
        assert len(formset._non_form_errors) == 1
        assert 'missing_management_form' in str(formset._non_form_errors[0])

    def test_full_clean_valid_data(self, formset):
        formset.data = {
            'form-0-integer_field': '1',
            'form-0-boolean_field': 'true',
            'form-1-integer_field': '2',
            'form-1-boolean_field': 'false',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '3',
        }
        formset.full_clean()
        assert not formset._non_form_errors
        assert all(isinstance(errors, ErrorList) for errors in formset.errors)

    def test_full_clean_too_many_forms(self, formset):
        formset.data = {
            'form-0-integer_field': '1',
            'form-1-integer_field': '2',
            'form-2-integer_field': '3',
            'form-TOTAL_FORMS': '4',  # Exceeds max_num
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '3',
        }
        with pytest.raises(ValidationError) as excinfo:
            formset.full_clean()
        
        assert 'too_many_forms' in str(excinfo.value)

    def test_full_clean_too_few_forms(self, formset):
        formset.data = {
            'form-0-integer_field': '1',
            'form-TOTAL_FORMS': '1',  # Less than min_num
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '3',
        }
        formset.min_num = 2  # Set min_num
        with pytest.raises(ValidationError) as excinfo:
            formset.full_clean()

        assert 'too_few_forms' in str(excinfo.value)

    def test_full_clean_empty_forms(self, formset):
        formset.data = {
            'form-0-integer_field': '',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '3',
        }
        formset.full_clean()
        assert len(formset._errors) == 1  # Expecting error for empty required field