import pytest
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey

class RelatedField(ForeignKey):
    def formfield(self, **kwargs):
        defaults = {}
        if hasattr(self.remote_field, 'get_related_field'):
            limit_choices_to = self.remote_field.limit_choices_to
            defaults.update({
                'limit_choices_to': limit_choices_to,
            })
        defaults.update(kwargs)
        return super().formfield(**defaults)

class TestRelatedField:
    @pytest.fixture
    def related_field(self):
        return RelatedField(User)

    def test_formfield_with_limit_choices_to(self, related_field):
        related_field.remote_field = type('RemoteField', (), {
            'get_related_field': lambda: None,
            'limit_choices_to': Q(is_active=True)
        })()

        form_field = related_field.formfield()
        assert isinstance(form_field, forms.ModelChoiceField)
        assert form_field.limit_choices_to == Q(is_active=True)

    def test_formfield_without_limit_choices_to(self, related_field):
        related_field.remote_field = type('RemoteField', (), {
            'get_related_field': lambda: None,
            'limit_choices_to': None
        })()

        form_field = related_field.formfield()
        assert isinstance(form_field, forms.ModelChoiceField)
        assert form_field.limit_choices_to is None

    def test_formfield_with_additional_kwargs(self, related_field):
        related_field.remote_field = type('RemoteField', (), {
            'get_related_field': lambda: None,
            'limit_choices_to': Q(is_active=True)
        })()

        form_field = related_field.formfield(widget=forms.Select)
        assert form_field.widget.__class__ is forms.Select
        assert form_field.limit_choices_to == Q(is_active=True)