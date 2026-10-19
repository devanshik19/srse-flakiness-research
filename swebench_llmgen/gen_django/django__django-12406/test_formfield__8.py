import pytest
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.db.models import ForeignKey

# Assuming RelatedField is part of a custom ForeignKeyField or similar that extends RelatedField
class RelatedField(models.ForeignKey):
    def formfield(self, **kwargs):
        defaults = {}
        if hasattr(self.remote_field, 'get_related_field'):
            limit_choices_to = self.remote_field.limit_choices_to
            defaults.update({'limit_choices_to': limit_choices_to})
        defaults.update(kwargs)
        return super().formfield(**defaults)

class TestRelatedFieldFormField:
    
    class TestModel(models.Model):
        user = RelatedField(User, related_name='test_related')

    class TestForm(ModelForm):
        class Meta:
            model = TestModel
            fields = ['user']

    def test_formfield_with_limit_choices_to(self):
        field_instance = TestModel._meta.get_field('user')
        field_instance.remote_field = type('RemoteField', (object,), {"limit_choices_to": Q()})

        form_field = field_instance.formfield()
        assert 'limit_choices_to' in form_field.__dict__
        assert form_field.__dict__['limit_choices_to'] == field_instance.remote_field.limit_choices_to

    def test_formfield_without_limit_choices_to(self):
        field_instance = TestModel._meta.get_field('user')
        field_instance.remote_field = type('RemoteField', (object,), {})

        form_field = field_instance.formfield()
        assert 'limit_choices_to' not in form_field.__dict__