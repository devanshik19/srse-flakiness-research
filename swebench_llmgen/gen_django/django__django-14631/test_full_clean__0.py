import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class TestBaseForm(forms.BaseForm):
    field1 = forms.CharField(required=True)
    field2 = forms.EmailField(required=False)

    def _clean_fields(self):
        for field_name, field in self.fields.items():
            value = self.cleaned_data.get(field_name)
            if field.required and not value:
                self.add_error(field_name, ValidationError("This field is required."))

    def _clean_form(self):
        pass  # Implement basic form cleaning as a placeholder

    def _post_clean(self):
        pass  # Implement post-cleaning logic if necessary

@pytest.mark.django_db
def test_full_clean_when_not_bound():
    form = TestBaseForm(data=None)
    form.full_clean()
    assert form.cleaned_data == {}
    assert not form.errors

@pytest.mark.django_db
def test_full_clean_with_no_changes_and_empty_permitted():
    form = TestBaseForm(data={}, empty_permitted=True)
    form.full_clean()
    assert form.cleaned_data == {}
    assert not form.errors

@pytest.mark.django_db
def test_full_clean_with_required_field_missing():
    form = TestBaseForm(data={'field2': 'test@example.com'})
    form.full_clean()
    assert 'field1' in form.errors
    assert form.errors['field1'] == [ValidationError("This field is required.")]

@pytest.mark.django_db
def test_full_clean_with_all_fields_valid():
    form = TestBaseForm(data={'field1': 'test', 'field2': 'test@example.com'})
    form.full_clean()
    assert 'field1' not in form.errors
    assert form.cleaned_data['field1'] == 'test'
    assert form.cleaned_data['field2'] == 'test@example.com'