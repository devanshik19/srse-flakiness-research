import pytest
from django.forms import Form
from django.forms.fields import BooleanField, IntegerField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

ORDERING_FIELD_NAME = 'order'
DELETION_FIELD_NAME = 'DELETE'

class TestForm(Form):
    pass

class TestBaseFormSet:
    def setup_method(self):
        self.formset = BaseFormSet(data={}, files={}, auto_id='id_%s', prefix='test', initial=[], error_class=None, form_kwargs={})

    def test_add_fields_with_ordering(self):
        form = TestForm()
        self.formset.can_order = True
        self.formset.initial_form_count = lambda: 2  # Mocking initial form count

        # Test with a valid index
        self.formset.add_fields(form, 0)
        assert isinstance(form.fields[ORDERING_FIELD_NAME], IntegerField)
        assert form.fields[ORDERING_FIELD_NAME].initial == 1
        
        # Test with an invalid index
        self.formset.add_fields(form, None)
        assert isinstance(form.fields[ORDERING_FIELD_NAME], IntegerField)
        assert form.fields[ORDERING_FIELD_NAME].initial is None

    def test_add_fields_with_deletion(self):
        form = TestForm()
        self.formset.can_delete = True
        self.formset.can_delete_extra = True
        self.formset.initial_form_count = lambda: 2  # Mocking initial form count

        self.formset.add_fields(form, 1)
        assert isinstance(form.fields[DELETION_FIELD_NAME], BooleanField)

    def test_add_fields_no_ordering_or_deletion(self):
        form = TestForm()
        self.formset.can_order = False
        self.formset.can_delete = False

        self.formset.add_fields(form, 1)
        assert ORDERING_FIELD_NAME not in form.fields
        assert DELETION_FIELD_NAME not in form.fields

    def test_add_fields_only_one_field_added(self):
        form = TestForm()
        self.formset.can_order = False
        self.formset.can_delete = True
        self.formset.can_delete_extra = True
        self.formset.initial_form_count = lambda: 0  # Mocking initial form count

        self.formset.add_fields(form, None)
        assert ORDERING_FIELD_NAME not in form.fields
        assert isinstance(form.fields[DELETION_FIELD_NAME], BooleanField)