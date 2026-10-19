import pytest
from django import forms
from django.contrib.auth.models import User
from django.db.models import ForeignKey
from django.forms.models import BaseModelFormSet, ModelChoiceField

class TestBaseModelFormSet(BaseModelFormSet):
    model = User
    edit_only = False
    unique_fields = []

    def __init__(self, data=None, files=None, auto_id=None, prefix=None, queryset=None):
        super().__init__(data, files, auto_id, prefix, queryset)

    def get_queryset(self):
        return User.objects.all()

def test_add_fields_with_editable_pk():
    formset = TestBaseModelFormSet()
    form = forms.Form()
    form.instance = User(username='testuser')
    form.instance.pk = 1
    form.is_bound = False
    index = None

    formset.add_fields(form, index)

    assert form.fields['id']  # Assuming 'id' is the field for the primary key
    assert isinstance(form.fields['id'], ModelChoiceField)

def test_add_fields_with_non_editable_pk():
    class NonEditableUserFormSet(TestBaseModelFormSet):
        def get_queryset(self):
            return User.objects.filter(username='non_editable_user')

    formset = NonEditableUserFormSet()
    form = forms.Form()
    form.instance = User(username='non_editable_user')
    form.instance.pk = None
    form.is_bound = False
    index = 0

    formset.add_fields(form, index)

    assert 'id' not in form.fields  # Ensure no primary key field added for non-editable pk

def test_add_fields_with_bound_form_and_index():
    User.objects.create(username='bound_user')
    formset = TestBaseModelFormSet()
    form = forms.Form()
    form.instance = User(username='bound_user')
    form.instance.pk = 1
    form.is_bound = True
    index = 0

    formset.add_fields(form, index)

    assert 'id' in form.fields  # Check if the primary key field is added
    assert form.fields['id'].queryset.count() == 1  # Should return the bound user