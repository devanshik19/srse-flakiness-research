import pytest
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms.models import ModelChoiceField
from django.forms import BaseFormSet

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class TestBaseModelFormSet(BaseFormSet):
    model = User

    def add_fields(self, form, index):
        super().add_fields(form, index)

@pytest.mark.parametrize("is_bound", [True, False])
def test_add_fields(is_bound):
    formset = TestBaseModelFormSet(data=None, files=None, queryset=User.objects.all())
    form = UserForm()
    form.instance = User(username='testuser') if not is_bound else User(username='existinguser')
    form.is_bound = is_bound
    formset.add_fields(form, index=None)

    # Check that a hidden field for the primary key is added
    assert form.fields['id'].widget.__class__ == forms.HiddenInput

    # Check if the initial value is set correctly for bound vs unbound form
    if is_bound:
        assert form.initial['id'] is None  # Assuming no user exists with pk None
    else:
        assert form.fields['id'].initial is None  # Placeholder for a new instance