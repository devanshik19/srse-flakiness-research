import pytest
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

@pytest.fixture
def user_formset():
    return modelformset_factory(User, form=UserForm, extra=2)

def test_modelformset_factory_creates_formset(user_formset):
    formset = user_formset(queryset=User.objects.none())
    assert formset is not None
    assert len(formset.forms) == 2

def test_modelformset_factory_no_fields_raises_exception():
    with pytest.raises(ImproperlyConfigured):
        modelformset_factory(User, form=ModelForm)

def test_modelformset_factory_with_exclude():
    formset = modelformset_factory(User, form=UserForm, exclude=['email'], extra=1)(queryset=User.objects.none())
    assert len(formset.forms) == 1
    assert 'email' not in formset.forms[0].fields

def test_modelformset_factory_with_extra_forms():
    formset = modelformset_factory(User, form=UserForm, extra=5)(queryset=User.objects.none())
    assert len(formset.forms) == 5

def test_modelformset_factory_with_invalid_model():
    with pytest.raises(TypeError):
        modelformset_factory(None, form=UserForm)