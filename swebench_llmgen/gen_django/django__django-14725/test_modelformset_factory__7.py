import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory

def test_modelformset_factory_fields():
    UserFormSet = modelformset_factory(User, fields=('username', 'email'))

    formset = UserFormSet(queryset=User.objects.all())
    assert formset.is_valid() is True
    assert len(formset) == 0  # No users in the database

def test_modelformset_factory_exclude():
    UserFormSet = modelformset_factory(User, exclude=('password',))

    formset = UserFormSet(queryset=User.objects.all())
    assert formset.is_valid() is True
    assert len(formset) == 0  # No users in the database

def test_modelformset_factory_invalid_with_no_fields():
    with pytest.raises(ImproperlyConfigured):
        modelformset_factory(User)

def test_modelformset_factory_valid_formset_with_extra():
    UserFormSet = modelformset_factory(User, fields=('username', 'email'), extra=2)

    formset = UserFormSet(queryset=User.objects.all())
    assert len(formset) == 2  # Should include 2 extra empty forms

def test_modelformset_factory_invalid_with_excluded_field():
    UserFormSet = modelformset_factory(User, fields=('username',), exclude=('email',))

    formset = UserFormSet(queryset=User.objects.all())
    assert formset.is_valid() is True

    # Checking form error for an excluded field
    form_data = {'form-0-username': 'testuser', 'form-0-email': ''}
    formset = UserFormSet(data=form_data)

    assert not formset.is_valid()
    assert 'email' not in formset.errors[0]

def test_modelformset_factory_with_invalid_form():
    UserFormSet = modelformset_factory(User, fields=('username', 'email'))
    form_data = {'form-0-username': '', 'form-0-email': 'invalidemail'}  # Username is empty

    formset = UserFormSet(data=form_data)
    assert not formset.is_valid()
    assert 'username' in formset.errors[0]