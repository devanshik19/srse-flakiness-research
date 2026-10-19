import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.forms import modelformset_factory

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

def test_modelformset_factory_valid():
    UserFormSet = modelformset_factory(User, form=UserForm, extra=2)
    formset = UserFormSet(queryset=User.objects.none())
    
    assert formset.is_valid() is True
    assert len(formset.forms) == 2

def test_modelformset_factory_no_fields():
    with pytest.raises(ImproperlyConfigured):
        modelformset_factory(User, form=UserForm)

def test_modelformset_factory_with_exclude():
    class ExcludingUserForm(forms.ModelForm):
        class Meta:
            model = User
            exclude = ['password']
    
    UserFormSet = modelformset_factory(User, form=ExcludingUserForm, extra=1)
    formset = UserFormSet(queryset=User.objects.none())
    
    assert formset.is_valid() is True
    assert len(formset.forms) == 1

def test_modelformset_factory_with_fields_and_exclude():
    with pytest.raises(ImproperlyConfigured):
        modelformset_factory(User, form=UserForm, fields=['username'], exclude=['email'])