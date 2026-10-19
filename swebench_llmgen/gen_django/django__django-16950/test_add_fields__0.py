import pytest
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms.models import ModelChoiceField
from django.forms import formset_factory

class TestForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class BaseModelFormSet:
    model = User

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
            if form.is_bound:
                pk_value = None if form.instance._state.adding else form.instance.pk
            else:
                try:
                    if index is not None:
                        pk_value = self.get_queryset()[index].pk
                    else:
                        pk_value = None
                except IndexError:
                    pk_value = None

            if isinstance(pk, (ForeignKey, OneToOneField)):
                qs = pk.remote_field.model._default_manager.get_queryset()
            else:
                qs = self.model._default_manager.get_queryset()
            qs = qs.using(form.instance._state.db)
            widget = form._meta.widgets.get(self._pk_field.name, forms.HiddenInput)
            form.fields[self._pk_field.name] = ModelChoiceField(
                qs, initial=pk_value, required=False, widget=widget
            )
        super().add_fields(form, index)

def test_add_fields_with_editable_pk():
    formset = formset_factory(TestForm)
    form = formset(data={'username': 'testuser'})
    form.instance = User(pk=1, username='testuser')  # Simulate existing user
    form.instance._state = models.ModelState(adding=False)
    
    formset_instance = BaseModelFormSet()
    formset_instance.add_fields(form, index=None)
    
    assert form.fields['id'].initial == 1  # pk should be populated with user's pk
    assert isinstance(form.fields['id'], ModelChoiceField)

def test_add_fields_with_non_editable_pk():
    class NonEditableModel(models.Model):
        id = models.AutoField(primary_key=True)

    class NonEditableForm(forms.ModelForm):
        class Meta:
            model = NonEditableModel
            fields = []

    formset = formset_factory(NonEditableForm)
    form = formset()
    form.instance = NonEditableModel()  # New instance, no pk assigned
    form.instance._state = models.ModelState(adding=True)
    
    formset_instance = BaseModelFormSet()
    formset_instance.model = NonEditableModel
    formset_instance.add_fields(form, index=None)

    assert 'id' in form.fields  # Should be added due to non-editable pk
    assert isinstance(form.fields['id'], ModelChoiceField)

def test_add_fields_existing_instance():
    existing_user = User.objects.create(username='existuser')
    formset = formset_factory(TestForm)
    form = formset(data={'username': 'existuser'})
    form.instance = existing_user
    form.instance._state = models.ModelState(adding=False)

    formset_instance = BaseModelFormSet()
    formset_instance.add_fields(form, index=None)

    assert form.fields['id'].initial == existing_user.pk  # Should match existing user's pk
    assert isinstance(form.fields['id'], ModelChoiceField)