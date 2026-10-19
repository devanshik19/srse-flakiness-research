import pytest
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.core.exceptions import ImproperlyConfigured

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

def test_modelformset_factory_no_fields_or_exclude():
    with pytest.raises(ImproperlyConfigured):
        modelformset_factory(User, form=UserForm)

def test_modelformset_factory_with_fields():
    UserFormSet = modelformset_factory(User, form=UserForm, fields=['username', 'email'])
    assert UserFormSet.model == User
    assert UserFormSet.form == UserForm

def test_modelformset_factory_with_exclude():
    UserFormSet = modelformset_factory(User, form=UserForm, exclude=['password'])
    assert UserFormSet.model == User
    assert UserFormSet.form == UserForm

def test_modelformset_factory_with_extra():
    UserFormSet = modelformset_factory(User, form=UserForm, extra=2)
    formset = UserFormSet(queryset=User.objects.none())
    assert len(formset.forms) == 2

def test_modelformset_factory_with_invalid_arguments():
    with pytest.raises(TypeError):
        modelformset_factory(User, form=UserForm, extra='invalid')