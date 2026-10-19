import pytest
from django.core.exceptions import ValidationError
from django.forms import Form, FormSet
from django.forms.fields import BooleanField, IntegerField
from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _

class SampleForm(Form):
    number = IntegerField(required=True)
    active = BooleanField(required=False)

class TestBaseFormSet:
    
    def setup_method(self):
        self.data_valid = [{'number': 1, 'active': True}, {'number': 2, 'active': False}]
        self.data_invalid = [{'number': '', 'active': True}, {'number': 3, 'active': False}]

    def test_full_clean_with_valid_data(self):
        formset = FormSet(form=SampleForm, data=self.data_valid)
        formset.full_clean()
        assert not formset.errors
        assert len(formset._non_form_errors) == 0

    def test_full_clean_with_invalid_data(self):
        formset = FormSet(form=SampleForm, data=self.data_invalid)
        formset.full_clean()
        assert len(formset.errors) == 2
        assert all(form_errors for form_errors in formset.errors)

    def test_full_clean_with_missing_management_form(self):
        # Simulating the absence of management form by not providing it
        formset = FormSet(form=SampleForm, data=[{'number': 1}])
        formset.full_clean()
        assert len(formset._non_form_errors) == 1
        assert isinstance(formset._non_form_errors[0], ValidationError)

    def test_full_clean_with_too_many_forms(self):
        formset = FormSet(form=SampleForm, data=[{'number': 1}] * 6)  # Assuming max_num is 5
        with pytest.raises(ValidationError):
            formset.full_clean()

    def test_full_clean_with_too_few_forms(self):
        formset = FormSet(form=SampleForm, data=[])  # Assuming min_num is 1
        with pytest.raises(ValidationError):
            formset.full_clean()