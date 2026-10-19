import pytest
from django import forms
from django.forms import BaseFormSet

ORDERING_FIELD_NAME = 'ORDERING_FIELD'
DELETION_FIELD_NAME = 'DELETION_FIELD'

class TestFormSet(BaseFormSet):
    can_order = True
    can_delete = True
    can_delete_extra = False

    def get_ordering_widget(self):
        return forms.NumberInput()

    def get_deletion_widget(self):
        return forms.CheckboxInput()

@pytest.mark.parametrize("index, expected_order, expected_delete", [
    (0, 1, True),    # First form in the initial forms
    (1, None, False), # Non-initial forms (extra)
    (None, None, True), # None index
])
def test_add_fields(index, expected_order, expected_delete):
    formset = TestFormSet(data={})
    form = forms.Form()
    formset.add_fields(form, index)

    # Check ordering field
    if expected_order is not None:
        assert isinstance(form.fields[ORDERING_FIELD_NAME], forms.IntegerField)
        assert form.fields[ORDERING_FIELD_NAME].initial == expected_order
    else:
        assert ORDERING_FIELD_NAME not in form.fields

    # Check deletion field
    if expected_delete:
        assert isinstance(form.fields[DELETION_FIELD_NAME], forms.BooleanField)
    else:
        assert DELETION_FIELD_NAME not in form.fields