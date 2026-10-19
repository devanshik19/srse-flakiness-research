import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.forms.models import modelformset_factory

def test_modelformset_factory_success():
    UserFormSet = modelformset_factory(User, extra=2, can_delete=True)
    formset = UserFormSet(queryset=User.objects.all())
    
    assert formset.is_valid() is True
    assert len(formset.forms) == 2  # Extra forms should be present

def test_modelformset_factory_without_fields():
    with pytest.raises(ImproperlyConfigured) as excinfo:
        modelformset_factory(User, form=forms.ModelForm)
    assert str(excinfo.value) == ("Calling modelformset_factory without defining 'fields' or "
                                   "'exclude' explicitly is prohibited.")

def test_modelformset_factory_with_fields():
    class UserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['username', 'email']
    
    UserFormSet = modelformset_factory(User, form=UserForm, extra=2)
    formset = UserFormSet(queryset=User.objects.all())
    
    assert len(formset.forms) == 2
    assert 'username' in formset.forms[0].fields
    assert 'email' in formset.forms[0].fields
    assert formset.is_valid() is True

def test_modelformset_factory_with_exclude():
    class UserForm(forms.ModelForm):
        class Meta:
            model = User
            exclude = ['password']
    
    UserFormSet = modelformset_factory(User, form=UserForm, extra=2)
    formset = UserFormSet(queryset=User.objects.all())
    
    assert len(formset.forms) == 2
    assert 'password' not in formset.forms[0].fields
    assert formset.is_valid() is True