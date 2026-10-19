import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.models import BaseModelFormSet
from django.db.models import AutoField, ForeignKey, OneToOneField

class TestBaseModelFormSet(BaseModelFormSet):
    model = User
    fields = '__all__'

@pytest.fixture
def user_formset():
    return TestBaseModelFormSet(data={}, files={})

def test_add_fields_with_editable_pk(user_formset):
    form = forms.ModelForm(data={'username': 'testuser'}, instance=User(username='existinguser'))
    user_formset.add_fields(form, None)
    assert user_formset._pk_field.name in form.fields
    assert isinstance(form.fields[user_formset._pk_field.name], forms.ModelChoiceField)

def test_add_fields_with_non_editable_pk(user_formset):
    user_formset.model._meta.pk.editable = False  # Simulating a non-editable primary key
    form = forms.ModelForm(data={'username': 'testuser'})
    user_formset.add_fields(form, None)
    assert user_formset._pk_field.name in form.fields
    assert isinstance(form.fields[user_formset._pk_field.name], forms.ModelChoiceField)

def test_add_fields_with_auto_created_pk(user_formset):
    class TestModelFormSet(BaseModelFormSet):
        model = User
        fields = '__all__'
        def get_queryset(self):
            return User.objects.none()  # Mock an empty queryset

    user_formset = TestModelFormSet(data={}, files={})
    form = forms.ModelForm(data={'username': 'testuser'})
    user_formset.add_fields(form, None)
    assert user_formset._pk_field.name in form.fields
    assert isinstance(form.fields[user_formset._pk_field.name], forms.ModelChoiceField)

def test_add_fields_with_bound_form(user_formset):
    user = User.objects.create(username='testuser')
    form = forms.ModelForm(data={'username': 'testuser'}, instance=user)
    form.is_bound = True
    user_formset.add_fields(form, None)
    assert form.fields[user_formset._pk_field.name].initial == user.pk