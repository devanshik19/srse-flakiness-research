import pytest
from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms.fields import BooleanField, IntegerField
from django.forms.widgets import CheckboxInput, HiddenInput, NumberInput
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.forms.formsets import BaseFormSet

ORDERING_FIELD_NAME = 'order'
DELETION_FIELD_NAME = 'delete'

class TestForm(Form):
    pass

class TestFormSet(BaseFormSet):
    can_order = True
    can_delete = True
    can_delete_extra = True

    def get_ordering_widget(self):
        return NumberInput()
    
    def get_deletion_widget(self):
        return CheckboxInput()

def test_add_fields_with_ordering_and_deletion():
    formset = TestFormSet(data={})
    form = TestForm()
    
    # Test with an index less than initial form count
    formset.initial_form_count = lambda: 3  # Mocking the count
    formset.add_fields(form, 1)
    assert ORDERING_FIELD_NAME in form.fields
    assert isinstance(form.fields[ORDERING_FIELD_NAME], IntegerField)
    assert form.fields[ORDERING_FIELD_NAME].initial == 2  # index + 1
    assert DELETION_FIELD_NAME in form.fields
    assert isinstance(form.fields[DELETION_FIELD_NAME], BooleanField)

    # Test with an index equal to or greater than initial form count
    formset.add_fields(form, 3)
    assert ORDERING_FIELD_NAME in form.fields  # Should still be present
    assert form.fields[ORDERING_FIELD_NAME].initial is None  # No initial value
    assert DELETION_FIELD_NAME in form.fields  # Should still be present

    # Test with can_delete_extra set to False
    formset.can_delete_extra = False
    formset.add_fields(form, 4)
    assert DELETION_FIELD_NAME not in form.fields  # Should not add deletion field