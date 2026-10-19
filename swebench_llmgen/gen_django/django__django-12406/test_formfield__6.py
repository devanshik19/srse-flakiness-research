import pytest
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

class RelatedField(models.Field):
    # Assuming other necessary field details and initializers exist here
    def formfield(self, **kwargs):
        defaults = {}
        if hasattr(self.remote_field, 'get_related_field'):
            limit_choices_to = self.remote_field.limit_choices_to
            defaults.update({
                'limit_choices_to': limit_choices_to,
            })
        defaults.update(kwargs)
        return super().formfield(**defaults)

class RelatedFieldTest(models.Model):
    related = RelatedField()

class RelatedFieldForm(ModelForm):
    class Meta:
        model = RelatedFieldTest
        fields = ['related']

def test_formfield_with_limit_choices_to():
    user = User.objects.create(username='testuser')
    related_field = RelatedField()
    related_field.remote_field = type('RemoteField', (), {"limit_choices_to": Q(pk=user.pk)})

    form_field = related_field.formfield()
    
    assert form_field.limit_choices_to == Q(pk=user.pk)

def test_formfield_without_limit_choices_to():
    related_field = RelatedField()
    related_field.remote_field = type('RemoteField', (), {})

    form_field = related_field.formfield()
    
    assert form_field.limit_choices_to is None