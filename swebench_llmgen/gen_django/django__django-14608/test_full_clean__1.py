import pytest
from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms.fields import BooleanField, IntegerField
from django.forms.utils import ErrorList
from django.forms.widgets import HiddenInput, NumberInput
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from django.contrib.auth.models import User

class TestForm(Form):
    name = BooleanField(required=True)
    age = IntegerField(required=True)

class TestBaseFormSet:
    def __init__(self, data=None):
        self.data = data or {}
        self.forms = [TestForm(data=self.data)]
        self._errors = []
        self._non_form_errors = ErrorList()
        self.management_form = self
        self.is_bound = bool(data)
        self.can_delete = True
        self.validate_max = True
        self.validate_min = True
        self.absolute_max = 10
        self.max_num = 5
        self.min_num = 1
        self.deleted_forms = []
    
    def is_valid(self):
        # Simplified validation for demonstration
        return all(form.is_valid() for form in self.forms)

    def initial_form_count(self):
        return 1

    def total_form_count(self):
        return len(self.forms)

    def _should_delete_form(self, form):
        return False

    def clean(self):
        if not self.forms[0].cleaned_data.get('name'):
            raise ValidationError('Name is required.')

@pytest.fixture
def valid_data():
    return {'name': True, 'age': 25}

@pytest.fixture
def invalid_data():
    return {'name': False}

def test_full_clean_valid(valid_data):
    formset = TestBaseFormSet(data=valid_data)
    formset.full_clean()
    assert not formset._errors
    assert not formset._non_form_errors

def test_full_clean_invalid(invalid_data):
    formset = TestBaseFormSet(data=invalid_data)
    formset.full_clean()
    assert formset._errors[0]['name']  # Expecting errors for 'name'
    assert len(formset._non_form_errors) == 0

def test_full_clean_too_many_forms(valid_data):
    formset = TestBaseFormSet(data={**valid_data, 'management_form-TOTAL_FORMS': 6})
    formset.full_clean()
    assert formset._non_form_errors
    assert isinstance(formset._non_form_errors[0], ValidationError)

def test_full_clean_too_few_forms(valid_data):
    formset = TestBaseFormSet(data={**valid_data, 'management_form-TOTAL_FORMS': 0})
    formset.full_clean()
    assert formset._non_form_errors
    assert isinstance(formset._non_form_errors[0], ValidationError)