import pytest
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

# Defining a test ModelForm for the User model
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

def test_modelformset_factory_creates_formset():
    UserFormSet = modelformset_factory(User, form=UserForm, extra=2)
    formset = UserFormSet(queryset=User.objects.none())
    assert formset.total_form_count() == 2

def test_modelformset_factory_no_fields_raises_error():
    with pytest.raises(ImproperlyConfigured):
        modelformset_factory(User, form=ModelForm)

def test_modelformset_factory_formset_attributes():
    UserFormSet = modelformset_factory(User, form=UserForm, extra=1)
    formset = UserFormSet(queryset=User.objects.none())
    assert hasattr(formset, 'model')
    assert formset.model == User

def test_modelformset_factory_with_exclude():
    UserFormSet = modelformset_factory(User, form=UserForm, fields=['username'], exclude=['email'])
    formset = UserFormSet(queryset=User.objects.none())
    assert 'email' not in formset.forms[0].fields

def test_modelformset_factory_with_non_existent_field_raises_error():
    class InvalidUserForm(ModelForm):
        class Meta:
            model = User
            fields = ['non_existent_field']

    with pytest.raises(ValueError):
        modelformset_factory(User, form=InvalidUserForm)

def test_modelformset_factory_validations():
    UserFormSet = modelformset_factory(User, form=UserForm, extra=1, max_num=5)
    formset = UserFormSet(queryset=User.objects.none())
    assert formset.max_num == 5