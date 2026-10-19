import pytest
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

def test_modelformset_factory_without_fields_or_exclude():
    with pytest.raises(ImproperlyConfigured, match="Calling modelformset_factory without defining 'fields' or 'exclude' explicitly is prohibited."):
        modelformset_factory(User)

def test_modelformset_factory_with_fields():
    formset_class = modelformset_factory(User, fields=['username'])
    formset = formset_class(queryset=User.objects.all())
    assert formset is not None
    assert len(formset.forms) == 1  # By default, extra is 1

def test_modelformset_factory_with_exclude():
    formset_class = modelformset_factory(User, exclude=['is_staff'])
    formset = formset_class(queryset=User.objects.all())
    assert formset is not None
    assert len(formset.forms) == 1  # By default, extra is 1

def test_modelformset_factory_with_extra_forms():
    formset_class = modelformset_factory(User, fields=['username'], extra=3)
    formset = formset_class(queryset=User.objects.all())
    assert formset is not None
    assert len(formset.forms) == 4  # 1 existing + 3 extra

def test_modelformset_factory_with_can_delete():
    formset_class = modelformset_factory(User, fields=['username'], can_delete=True)
    formset = formset_class(queryset=User.objects.all())
    assert formset can_delete == True  # Check if can_delete is set correctly