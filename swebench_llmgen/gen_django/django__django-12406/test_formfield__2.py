import pytest
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.db.models.fields.related import RelatedField


class TestRelatedField(RelatedField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.remote_field = models.ForeignKey(User, on_delete=models.CASCADE)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


def test_formfield_with_limit_choices_to():
    field = TestRelatedField()
    field.remote_field.limit_choices_to = Q(is_active=True)

    form_field = field.formfield()
    
    assert form_field is not None
    assert form_field.limit_choices_to == Q(is_active=True)


def test_formfield_without_limit_choices_to():
    field = TestRelatedField()
    field.remote_field.limit_choices_to = None

    form_field = field.formfield()

    assert form_field is not None
    assert 'limit_choices_to' not in form_field.__dict__