import pytest
from django.forms import Form
from django.forms.fields import BooleanField, IntegerField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.forms import BaseFormSet

ORDERING_FIELD_NAME = 'order'
DELETION_FIELD_NAME = 'DELETE'

class DummyFormSet(BaseFormSet):
    can_order = True
    can_delete = True
    can_delete_extra = False

    def get_deletion_widget(self):
        return CheckboxInput()

    def get_ordering_widget(self):
        return NumberInput()

    def initial_form_count(self):
        return 2

def test_add_fields_with_ordering_and_deletion():
    formset = DummyFormSet(data=None, files=None, auto_id=None, prefix=None, initial=None, error_class=None, form_kwargs=None, error_messages=None)
    
    form1 = Form()
    form2 = Form()
    form3 = Form()
    
    formset.add_fields(form1, 0)
    formset.add_fields(form2, 1)
    formset.add_fields(form3, None)

    # Test ordering field for initial forms
    assert ORDERING_FIELD_NAME in form1.fields
    assert form1.fields[ORDERING_FIELD_NAME].initial == 1  # index 0 + 1
    assert ORDERING_FIELD_NAME in form2.fields
    assert form2.fields[ORDERING_FIELD_NAME].initial == 2  # index 1 + 1

    # Test no ordering field for forms beyond initial forms
    assert ORDERING_FIELD_NAME in form3.fields
    assert form3.fields[ORDERING_FIELD_NAME].initial is None

    # Test deletion field for initial forms
    assert DELETION_FIELD_NAME in form1.fields
    assert isinstance(form1.fields[DELETION_FIELD_NAME], BooleanField)

    assert DELETION_FIELD_NAME in form2.fields
    assert isinstance(form2.fields[DELETION_FIELD_NAME], BooleanField)

    # Test no deletion field for form3
    assert DELETION_FIELD_NAME in form3.fields
    assert isinstance(form3.fields[DELETION_FIELD_NAME], BooleanField)