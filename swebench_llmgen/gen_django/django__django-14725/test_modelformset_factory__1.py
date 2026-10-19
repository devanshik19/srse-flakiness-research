import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory

def test_modelformset_factory_with_fields():
    UserFormSet = modelformset_factory(User, fields=('username', 'email'), extra=2)
    formset = UserFormSet(queryset=User.objects.all())
    
    assert formset.extra == 2
    assert all(isinstance(form, forms.ModelForm) for form in formset.forms)

def test_modelformset_factory_with_exclude():
    UserFormSet = modelformset_factory(User, exclude=('password',), extra=1)
    formset = UserFormSet(queryset=User.objects.all())
    
    assert formset.extra == 1
    assert all('password' not in form.fields for form in formset.forms)

def test_modelformset_factory_no_fields_or_exclude():
    with pytest.raises(ImproperlyConfigured):
        modelformset_factory(User)

def test_modelformset_factory_with_invalid_form():
    class InvalidForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ()  # No fields defined, should raise an error

    with pytest.raises(ImproperlyConfigured):
        modelformset_factory(User, form=InvalidForm)

def test_modelformset_factory_with_custom_formset():
    CustomFormSet = modelformset_factory(User, extra=1, formset=forms.BaseFormSet)
    formset = CustomFormSet(queryset=User.objects.all())
    
    assert isinstance(formset, forms.BaseFormSet)
    assert formset.extra == 1