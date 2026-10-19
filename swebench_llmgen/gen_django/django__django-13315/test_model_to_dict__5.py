import warnings
from itertools import chain
from django.core.exceptions import (
    NON_FIELD_ERRORS, FieldError, ImproperlyConfigured, ValidationError,
)
from django.forms.fields import ChoiceField, Field
from django.forms.forms import BaseForm, DeclarativeFieldsMetaclass
from django.forms.formsets import BaseFormSet, formset_factory
from django.forms.utils import ErrorList
from django.forms.widgets import (
    HiddenInput, MultipleHiddenInput, RadioSelect, SelectMultiple,
)
from django.utils.deprecation import RemovedInDjango40Warning
from django.utils.text import capfirst, get_text_list
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.models import User
import pytest

def model_to_dict(instance, fields=None, exclude=None):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if not getattr(f, 'editable', False):
            continue
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)
    return data

@pytest.mark.django_db
def test_model_to_dict():
    user = User.objects.create_user(username='testuser', password='password')
    
    # Test without fields or exclude
    result = model_to_dict(user)
    assert result['username'] == 'testuser'
    assert 'password' not in result
    assert 'last_login' not in result
    assert 'is_superuser' in result
    assert 'is_staff' in result

    # Test with fields
    result = model_to_dict(user, fields=['username', 'is_active'])
    assert result == {'username': 'testuser', 'is_active': True}

    # Test with exclude
    result = model_to_dict(user, exclude=['username'])
    assert 'username' not in result
    assert 'is_active' in result

    # Test with both fields and exclude
    result = model_to_dict(user, fields=['username', 'is_active'], exclude=['is_active'])
    assert result == {'username': 'testuser'}

    # Test with no fields
    result = model_to_dict(user, fields=[])
    assert result == {}

    # Test warning for improperly configured model
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        # Assuming a model that is not properly set up
        result = model_to_dict(user, fields=['non_existent_field'])
        assert len(w) == 0  # Ensure no warnings were raised