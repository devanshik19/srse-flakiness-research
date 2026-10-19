import pytest
from django.contrib.auth.models import User
from django.forms import Form
from django.forms.fields import BooleanField, IntegerField
from django.utils.translation import gettext_lazy as _
from django.forms.formsets import BaseFormSet

ORDERING_FIELD_NAME = 'order'
DELETION_FIELD_NAME = 'DELETE'


class TestForm(Form):
    name = IntegerField()


class TestBaseFormSet(BaseFormSet):
    can_order = True
    can_delete = True
    can_delete_extra = False
    deletion_widget = BooleanField()
    ordering_widget = IntegerField()

    def get_deletion_widget(self):
        return self.deletion_widget

    def get_ordering_widget(self):
        return self.ordering_widget


@pytest.mark.parametrize("index, expected_order_initial, expected_order_later, should_have_deletion_field", [
    (0, 1, None, True),  # Initial form (index within initial form count)
    (1, None, None, False),  # Extra form (index >= initial form count)
    (None, None, None, True),  # No index provided
])
def test_add_fields(index, expected_order_initial, expected_order_later, should_have_deletion_field):
    formset = TestBaseFormSet(data={}, auto_id='id_%s', prefix='test', initial=[], error_class=None,
                              form_kwargs=None, error_messages={})
    
    form = TestForm()
    
    # Mock the initial_form_count method to return a count of 2 for the test.
    formset.initial_form_count = lambda: 2

    formset.add_fields(form, index)

    # Check ordering field
    if expected_order_initial is not None:
        assert ORDERING_FIELD_NAME in form.fields
        assert isinstance(form.fields[ORDERING_FIELD_NAME], IntegerField)
        assert form.fields[ORDERING_FIELD_NAME].initial == expected_order_initial
    else:
        assert ORDERING_FIELD_NAME not in form.fields

    # Check deletion field
    if should_have_deletion_field:
        assert DELETION_FIELD_NAME in form.fields
        assert isinstance(form.fields[DELETION_FIELD_NAME], BooleanField)
    else:
        assert DELETION_FIELD_NAME not in form.fields