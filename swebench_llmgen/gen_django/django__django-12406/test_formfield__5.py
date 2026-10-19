import pytest
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
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
    def test_formfield_with_limit_choices_to(self):
        class TestModel(models.Model):
            user = RelatedField(User, limit_choices_to={'is_active': True})

        class TestModelForm(ModelForm):
            class Meta:
                model = TestModel
                fields = ['user']

        form = TestModelForm()
        field = form.fields['user']
        assert 'limit_choices_to' in field.widget.attrs
        assert field.widget.attrs['limit_choices_to'] == {'is_active': True}

    def test_formfield_without_limit_choices_to(self):
        class TestModel(models.Model):
            user = RelatedField(User)

        class TestModelForm(ModelForm):
            class Meta:
                model = TestModel
                fields = ['user']

        form = TestModelForm()
        field = form.fields['user']
        assert 'limit_choices_to' not in field.widget.attrs