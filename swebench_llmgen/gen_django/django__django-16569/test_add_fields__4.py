import pytest
from django.contrib.auth.models import User
from django.forms import Form
from django.forms.fields import BooleanField, IntegerField
from django.utils.translation import gettext_lazy as _
from django.forms.formsets import BaseFormSet

ORDERING_FIELD_NAME = 'order'
DELETION_FIELD_NAME = 'DELETE'

class TestForm(Form):
    pass

class TestFormSet(BaseFormSet):
    can_order = True
    can_delete = True
    can_delete_extra = True

    def get_deletion_widget(self):
        return CheckboxInput()

    def get_ordering_widget(self):
        return NumberInput()

def test_add_fields_with_ordering_and_deletion():
    formset = TestFormSet(data=None, files=None, auto_id='id_%s', prefix='test', initial=[], error_class=None, form_kwargs={})
    form = TestForm()

    formset.add_fields(form, 0)

    assert ORDERING_FIELD_NAME in form.fields
    assert isinstance(form.fields[ORDERING_FIELD_NAME], IntegerField)
    assert form.fields[ORDERING_FIELD_NAME].label == _("Order")
    assert form.fields[ORDERING_FIELD_NAME].initial == 1
    assert not form.fields[ORDERING_FIELD_NAME].required

    assert DELETION_FIELD_NAME in form.fields
    assert isinstance(form.fields[DELETION_FIELD_NAME], BooleanField)
    assert form.fields[DELETION_FIELD_NAME].label == _("Delete")
    assert not form.fields[DELETION_FIELD_NAME].required

def test_add_fields_without_ordering_and_deletion():
    formset = TestFormSet(data=None, files=None, auto_id='id_%s', prefix='test', initial=[], error_class=None, form_kwargs={})
    form = TestForm()

    formset.add_fields(form, 1)

    assert ORDERING_FIELD_NAME in form.fields
    assert isinstance(form.fields[ORDERING_FIELD_NAME], IntegerField)
    assert form.fields[ORDERING_FIELD_NAME].label == _("Order")
    assert form.fields[ORDERING_FIELD_NAME].initial is None
    assert not form.fields[ORDERING_FIELD_NAME].required

    assert DELETION_FIELD_NAME in form.fields
    assert isinstance(form.fields[DELETION_FIELD_NAME], BooleanField)
    assert form.fields[DELETION_FIELD_NAME].label == _("Delete")
    assert not form.fields[DELETION_FIELD_NAME].required