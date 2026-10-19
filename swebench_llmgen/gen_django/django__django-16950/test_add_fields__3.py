import pytest
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms.models import BaseModelFormSet
from django.forms.models import ModelChoiceField

class TestBaseModelFormSet(BaseModelFormSet):
    model = User

@pytest.fixture
def formset():
    return TestBaseModelFormSet(queryset=User.objects.all())

def test_add_fields_pk_not_editable(formset):
    # Create a form instance for the User model
    class UserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['username']

    form = UserForm()
    
    # Test when form is not bound and pk field is not editable
    formset.add_fields(form, None)
    assert form.fields['id']  # Check that the primary key field is added
    assert isinstance(form.fields['id'], ModelChoiceField)

def test_add_fields_pk_is_editable(formset):
    class UserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['username']

    form = UserForm()
    form.instance = User(username='testuser')
    formset.add_fields(form, None)
    assert 'id' not in form.fields  # Editable pk should not be added

def test_add_fields_with_bound_form(formset):
    class UserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['username']

    user = User.objects.create(username='testuser')
    form = UserForm(instance=user)
    form.is_bound = True
    formset.add_fields(form, None)
    
    # Check that the primary key field is added
    assert form.fields['id']  # Primary key field should be added
    assert form.fields['id'].initial == user.pk  # Initial value should be user's pk