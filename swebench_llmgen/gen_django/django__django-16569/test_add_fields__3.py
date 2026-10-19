import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms.fields import BooleanField, IntegerField
from django.forms.widgets import CheckboxInput, NumberInput
from django.utils.translation import gettext_lazy as _

ORDERING_FIELD_NAME = 'ORDERING_FIELD_NAME'
DELETION_FIELD_NAME = 'DELETION_FIELD_NAME'

class TestForm(Form):
    pass

class TestBaseFormSet:
    can_order = True
    can_delete = True
    can_delete_extra = True

    def initial_form_count(self):
        return 2

    def get_ordering_widget(self):
        return NumberInput()

    def get_deletion_widget(self):
        return CheckboxInput()

    def add_fields(self, form, index):
        initial_form_count = self.initial_form_count()
        if self.can_order:
            if index is not None and index < initial_form_count:
                form.fields[ORDERING_FIELD_NAME] = IntegerField(
                    label=_("Order"),
                    initial=index + 1,
                    required=False,
                    widget=self.get_ordering_widget(),
                )
            else:
                form.fields[ORDERING_FIELD_NAME] = IntegerField(
                    label=_("Order"),
                    required=False,
                    widget=self.get_ordering_widget(),
                )
        if self.can_delete and (self.can_delete_extra or index < initial_form_count):
            form.fields[DELETION_FIELD_NAME] = BooleanField(
                label=_("Delete"),
                required=False,
                widget=self.get_deletion_widget(),
            )

@pytest.mark.parametrize("index, expected_ordering_field, expected_deletion_field", [
    (0, True, True),  # existing form with ordering and deletion field
    (1, True, True),  # existing form with ordering and deletion field
    (2, True, True),  # new form with only ordering field
    (None, True, True),  # new form with only ordering field
])
def test_add_fields(index, expected_ordering_field, expected_deletion_field):
    formset = TestBaseFormSet()
    form = TestForm()
    formset.add_fields(form, index)

    assert (ORDERING_FIELD_NAME in form.fields) == expected_ordering_field
    assert (DELETION_FIELD_NAME in form.fields) == expected_deletion_field
    if expected_ordering_field:
        assert isinstance(form.fields[ORDERING_FIELD_NAME], IntegerField)
    if expected_deletion_field:
        assert isinstance(form.fields[DELETION_FIELD_NAME], BooleanField)