import pytest
from django.contrib.auth.models import User
from django.forms import ModelForm, Form
from django.forms.models import BaseModelFormSet, ModelChoiceField
from django.forms.widgets import HiddenInput
from django.core.exceptions import ValidationError


class TestForm(Form):
    pass


class TestModelFormSet(BaseModelFormSet):
    model = User

    def _construct_form(self, i, **kwargs):
        form = super()._construct_form(i, **kwargs)
        self.add_fields(form, i)
        return form


def test_add_fields_with_editable_pk():
    formset = TestModelFormSet(queryset=User.objects.all())
    user_instance = User.objects.create(username='testuser', password='password123')
    form = formset._construct_form(0, instance=user_instance)
    
    assert form.fields['id'].widget.__class__ == HiddenInput
    assert form['id'].value() == str(user_instance.pk)


def test_add_fields_with_non_editable_pk():
    class NonEditableFormSet(BaseModelFormSet):
        model = User

        def _construct_form(self, i, **kwargs):
            if 'instance' in kwargs and kwargs['instance'] is not None:
                kwargs['instance']._state.adding = False
            form = super()._construct_form(i, **kwargs)
            self.add_fields(form, i)
            return form

    user_instance = User.objects.create(username='testuser2', password='password123')
    formset = NonEditableFormSet(queryset=User.objects.all())
    form = formset._construct_form(0, instance=user_instance)

    assert 'id' not in form.fields


def test_add_fields_for_new_instance():
    formset = TestModelFormSet(queryset=User.objects.none())
    form = formset._construct_form(0, instance=User())
    
    assert form.fields['id'].widget.__class__ == HiddenInput
    assert form['id'].value() is None


def test_add_fields_for_index_error():
    formset = TestModelFormSet(queryset=User.objects.all())
    form = formset._construct_form(99, instance=None)

    # Expecting it to still add the hidden field, but the value should be None
    assert form.fields['id'].widget.__class__ == HiddenInput
    assert form['id'].value() is None