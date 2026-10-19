import pytest
from itertools import chain
from django.core.exceptions import (
    NON_FIELD_ERRORS,
    FieldError,
    ImproperlyConfigured,
    ValidationError,
)
from django.db import models
from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from django.contrib.auth.models import User

class TestBaseModelFormSet:
    class BaseModelFormSet:
        model = User

        def __init__(self, data=None, files=None, auto_id=None, prefix=None, queryset=None):
            self.data = data
            self.files = files
            self.auto_id = auto_id
            self.prefix = prefix
            self.queryset = queryset or self.model.objects.all()
            self._pk_field = self.model._meta.pk

        def get_queryset(self):
            return self.queryset

        def add_fields(self, form, index):
            from django.db.models import AutoField, ForeignKey, OneToOneField
            self._pk_field = pk = self.model._meta.pk

            def pk_is_not_editable(pk):
                return (
                    (not pk.editable)
                    or (pk.auto_created or isinstance(pk, AutoField))
                    or (
                        pk.remote_field
                        and pk.remote_field.parent_link
                        and pk_is_not_editable(pk.remote_field.model._meta.pk)
                    )
                )

            if pk_is_not_editable(pk) or pk.name not in form.fields:
                pk_value = None if form.instance._state.adding else form.instance.pk
                if index is not None:
                    pk_value = self.get_queryset()[index].pk
                qs = pk.remote_field.model._default_manager.get_queryset() if isinstance(pk, (ForeignKey, OneToOneField)) else self.model._default_manager.get_queryset()
                form.fields[self._pk_field.name] = ModelForm.model_choice_field(qs, initial=pk_value, required=False, widget=HiddenInput)
    
    class TestForm(ModelForm):
        class Meta:
            model = User
            fields = ['username']  # Taking one field for the test

    def test_add_fields_with_editable_pk(self):
        formset = self.BaseModelFormSet()
        form = self.TestForm(instance=User(username='testuser'))
        formset.add_fields(form, None)
        assert form._pk_field.name in form.fields
        assert isinstance(form.fields[formset._pk_field.name].widget, HiddenInput)

    def test_add_fields_with_non_editable_pk(self):
        user_instance = User.objects.create(username='testuser')
        formset = self.BaseModelFormSet()
        form = self.TestForm(instance=user_instance)
        formset.add_fields(form, None)
        assert formset._pk_field.name in form.fields
        assert form.fields[formset._pk_field.name].initial == user_instance.pk