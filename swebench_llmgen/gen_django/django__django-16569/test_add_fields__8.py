import pytest
from django.forms import Form
from django.forms.fields import BooleanField, IntegerField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.forms import BaseFormSet

ORDERING_FIELD_NAME = 'order'
DELETION_FIELD_NAME = 'DELETE'


class TestForm(Form):
    pass


class TestBaseFormSet(BaseFormSet):
    can_order = True
    can_delete = True
    can_delete_extra = False

    def get_ordering_widget(self):
        return NumberInput()

    def get_deletion_widget(self):
        return CheckboxInput()


@pytest.fixture
def formset():
    return TestBaseFormSet(data={}, files={}, auto_id='id_%s', prefix='test', initial=[], error_class=None, form_kwargs={})


def test_add_fields_with_ordering(formset):
    form = TestForm()
    formset.add_fields(form, 0)
    assert ORDERING_FIELD_NAME in form.fields
    assert isinstance(form.fields[ORDERING_FIELD_NAME], IntegerField)
    assert form.fields[ORDERING_FIELD_NAME].initial == 1

    formset.add_fields(form, None)
    assert ORDERING_FIELD_NAME in form.fields
    assert form.fields[ORDERING_FIELD_NAME].initial is None


def test_add_fields_with_deletion(formset):
    form = TestForm()
    formset.add_fields(form, 0)
    assert DELETION_FIELD_NAME in form.fields
    assert isinstance(form.fields[DELETION_FIELD_NAME], BooleanField)

    formset.can_delete_extra = True
    formset.add_fields(form, 1)
    assert DELETION_FIELD_NAME in form.fields