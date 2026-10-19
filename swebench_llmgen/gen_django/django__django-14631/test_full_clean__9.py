import pytest
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class TestBaseForm(forms.BaseForm):
    def __init__(self, data=None, *args, **kwargs):
        self.is_bound = bool(data)
        self.data = data or {}
        self.cleaned_data = {}
        self._errors = forms.ErrorDict()
        self.empty_permitted = kwargs.get('empty_permitted', False)
        super().__init__(*args, **kwargs)

    def has_changed(self):
        return True  # Simulate that data has changed for testing.

    def _clean_fields(self):
        # Simulate a field cleaning process. Will raise ValidationError for testing.
        if 'name' not in self.data:
            self.add_error('name', ValidationError("This field is required."))

    def _clean_form(self):
        pass

    def _post_clean(self):
        pass

@pytest.mark.parametrize(
    'data, expected_errors, expected_cleaned_data',
    [
        (None, {}, {}),  # Not bound
        ({'name': 'John'}, {}, {'name': 'John'}),  # Valid data
        ({}, {'name': ['This field is required.']}, {}),  # Missing field
    ]
)
def test_full_clean(data, expected_errors, expected_cleaned_data):
    form = TestBaseForm(data=data)

    form.full_clean()

    assert form._errors.as_data() == expected_errors
    assert form.cleaned_data == expected_cleaned_data