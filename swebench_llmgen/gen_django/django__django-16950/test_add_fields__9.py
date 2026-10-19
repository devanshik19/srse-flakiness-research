import pytest
from django import forms
from django.contrib.auth.models import User
from django.db.models import ForeignKey, OneToOneField, AutoField
from django.forms import ModelForm
from django.forms.models import BaseModelFormSet

class TestUserFormSet(BaseModelFormSet):
    model = User

class TestForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']

@pytest.fixture
def user_formset():
    return TestUserFormSet(queryset=User.objects.none())

def test_add_fields_pk_editable(user_formset):
    form = TestForm(data={'username': 'testuser'})
    user_formset.add_fields(form, None)
    assert 'id' in form.fields  # Check if the PK field is added
    
    # Simulating a valid user and checking the binding
    user = User.objects.create(username='testuser')
    form.instance = user
    form.is_bound = True
    
    user_formset.add_fields(form, None)
    assert form.fields['id'].initial is None  # PK should be None when adding

def test_add_fields_with_existing_user(user_formset):
    user = User.objects.create(username='testuser')
    form = TestForm(data={'username': 'updateduser'})
    form.instance = user
    form.is_bound = True

    user_formset.add_fields(form, 0)
    assert form.fields['id'].initial == user.pk  # Check if initialized with the user's PK

def test_add_fields_no_pk_defined(user_formset):
    form = TestForm(data={'username': 'testuser'})
    form.instance = User()  # New instance, simulating a user that has not been saved
    form.is_bound = True
    
    user_formset.add_fields(form, None)
    assert 'id' not in form.fields  # PK should not be added for new unsaved instance