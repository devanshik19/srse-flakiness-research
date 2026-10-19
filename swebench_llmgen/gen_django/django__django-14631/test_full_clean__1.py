import pytest
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDict

class TestBaseForm(forms.BaseForm):
    def __init__(self, data=None):
        self.data = data or MultiValueDict()
        self.is_bound = bool(data)
        self.cleaned_data = {}
        self._errors = forms.ErrorDict()
        self.empty_permitted = False

    def has_changed(self):
        # Simulating a changed check; return False for our basic tests
        return False

    def _clean_fields(self):
        # Simulating successful field cleaning
        if 'name' not in self.data:
            self.add_error(None, 'This field is required.')
        else:
            self.cleaned_data['name'] = self.data['name']

    def _clean_form(self):
        pass  # Assume form cleaning logic here

    def _post_clean(self):
        pass  # Assume post cleaning logic here

@pytest.mark.parametrize("data, expected_errors, expected_cleaned_data", [
    (None, {}, {}),  # When no data is provided
    (MultiValueDict({'name': 'Test User'}), {}, {'name': 'Test User'}),  # Valid data
    (MultiValueDict({}), {'non_field_errors': ['This field is required.']}, {})  # Missing field
])
def test_full_clean(data, expected_errors, expected_cleaned_data):
    form = TestBaseForm(data)

    form.full_clean()

    assert dict(form._errors) == expected_errors
    assert form.cleaned_data == expected_cleaned_data