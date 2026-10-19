import pytest
from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.db.models import ForeignKey

class RelatedField(ForeignKey):
    # The given code of the `formfield` method should be inside this class
    def formfield(self, **kwargs):
        defaults = {}
        if hasattr(self.remote_field, 'get_related_field'):
            limit_choices_to = self.remote_field.limit_choices_to
            defaults.update({
                'limit_choices_to': limit_choices_to,
            })
        defaults.update(kwargs)
        return super().formfield(**defaults)

@pytest.mark.django_db
def test_formfield_with_limit_choices_to():
    user_field = RelatedField(User, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    form_field = user_field.formfield()
    
    # Check if the correct limit_choices_to is passed
    assert isinstance(form_field, forms.ModelChoiceField)
    assert form_field.limit_choices_to == {'is_active': True}

@pytest.mark.django_db
def test_formfield_without_limit_choices_to():
    user_field = RelatedField(User, on_delete=models.CASCADE)
    form_field = user_field.formfield()
    
    # Check if no limit_choices_to is passed
    assert isinstance(form_field, forms.ModelChoiceField)
    assert form_field.limit_choices_to is None