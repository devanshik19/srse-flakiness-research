import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from django.core.exceptions import ImproperlyConfigured


def test_modelformset_factory_with_fields():
    class UserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['username', 'email']

    UserFormSet = modelformset_factory(User, form=UserForm, extra=2)
    formset = UserFormSet(queryset=User.objects.none())
    
    # Test the number of forms
    assert len(formset) == 2
    assert isinstance(formset.forms[0], UserForm)


def test_modelformset_factory_with_exclude():
    class UserForm(forms.ModelForm):
        class Meta:
            model = User
            exclude = ['last_login']

    UserFormSet = modelformset_factory(User, form=UserForm, extra=1)
    formset = UserFormSet(queryset=User.objects.none())

    # Test that fields are properly excluded
    assert 'last_login' not in formset.forms[0].fields


def test_modelformset_factory_without_fields_or_exclude():
    with pytest.raises(ImproperlyConfigured) as excinfo:
        modelformset_factory(User, form=forms.ModelForm, extra=1)
    assert str(excinfo.value) == (
        "Calling modelformset_factory without defining 'fields' or "
        "'exclude' explicitly is prohibited."
    )


def test_modelformset_factory_validations():
    class UserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['username', 'email']

    UserFormSet = modelformset_factory(User, form=UserForm, extra=1)

    # Creating formset with invalid data
    data = {
        'form-0-username': '',
        'form-0-email': 'not-an-email',
    }
    formset = UserFormSet(data=data)

    assert not formset.is_valid()
    assert 'username' in formset.errors[0]
    assert 'email' in formset.errors[0]


def test_modelformset_factory_with_custom_formset():
    class UserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['username', 'email']

    class CustomFormSet(forms.BaseFormSet):
        def clean(self):
            if any(self.errors):
                return
            # Custom cleaning logic, for example:
            if self.total_form_count() < 1:
                raise forms.ValidationError('At least one user must be added.')

    UserFormSet = modelformset_factory(User, form=UserForm, formset=CustomFormSet, extra=1)
    formset = UserFormSet(queryset=User.objects.none())

    assert isinstance(formset, CustomFormSet)