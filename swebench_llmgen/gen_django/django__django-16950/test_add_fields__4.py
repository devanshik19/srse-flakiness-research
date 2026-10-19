import pytest
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms.models import BaseModelFormSet, ModelChoiceField

class TestFormSet(BaseModelFormSet):
    model = User

def test_add_fields_with_non_editable_pk():
    formset = TestFormSet(queryset=User.objects.all())
    form = forms.Form()
    form.instance = User(username='testuser')
    form.instance._state.adding = False
    formset.add_fields(form, None)

    assert form.fields['id']  # Assuming 'id' is the primary key field
    assert isinstance(form.fields['id'], ModelChoiceField)

def test_add_fields_with_editable_pk():
    formset = TestFormSet(queryset=User.objects.all())
    form = forms.Form()
    form.instance = User(username='testuser')
    form.instance._state.adding = True
    formset.add_fields(form, None)

    assert 'id' not in form.fields  # Editable pk should not be included

def test_add_fields_with_bound_form_and_existing_instance():
    user = User.objects.create(username='existinguser')
    formset = TestFormSet(queryset=User.objects.all())
    form = forms.Form(data={'username': 'existinguser'})
    form.instance = user
    form.instance._state.adding = False
    formset.add_fields(form, None)

    assert form.fields['id'].initial == user.id  # Should set PK value from existing instance

def test_add_fields_with_index():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    formset = TestFormSet(queryset=User.objects.all())
    form = forms.Form()
    form.instance = user1
    formset.add_fields(form, 1)

    assert form.fields['id'].initial == user2.id  # Should set PK value of user2 at index 1

def test_add_fields_with_no_queryset():
    formset = TestFormSet(queryset=User.objects.none())
    form = forms.Form()
    form.instance = User(username='nouser')
    formset.add_fields(form, None)

    assert form.fields['id']  # PK field still added even if queryset is empty