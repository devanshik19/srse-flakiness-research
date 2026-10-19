import pytest
from django.forms import Form
from django.forms.fields import BooleanField, IntegerField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.forms import BaseFormSet

ORDERING_FIELD_NAME = 'order'
DELETION_FIELD_NAME = 'DELETE'

class TestFormSet(BaseFormSet):
    can_order = True
    can_delete = True
    can_delete_extra = True

    def get_deletion_widget(self):
        return CheckboxInput()

    def get_ordering_widget(self):
        return NumberInput()

@pytest.mark.parametrize("index, expected_order_initial, expected_order_field", [
    (0, 1, True),  # Initial form
    (1, None, False),  # Extra form
    (None, None, False),  # No index
])
def test_add_fields(index, expected_order_initial, expected_order_field):
    formset = TestFormSet(data={}, files={}, auto_id='id_%s', prefix='test', initial=[], error_class=None, form_kwargs={})
    form = Form()
    formset.add_fields(form, index)

    if expected_order_field:
        assert ORDERING_FIELD_NAME in form.fields
        assert isinstance(form.fields[ORDERING_FIELD_NAME], IntegerField)
        assert form.fields[ORDERING_FIELD_NAME].initial == expected_order_initial
    else:
        assert ORDERING_FIELD_NAME not in form.fields

    if formset.can_delete and (formset.can_delete_extra or (index is not None and index < 0)):
        assert DELETION_FIELD_NAME in form.fields
        assert isinstance(form.fields[DELETION_FIELD_NAME], BooleanField)
    else:
        assert DELETION_FIELD_NAME not in form.fields