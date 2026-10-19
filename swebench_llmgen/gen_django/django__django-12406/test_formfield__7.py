import pytest
from django.contrib.auth.models import User
from django.db import models
from django import forms

# A simple related field subclass for testing
class TestRelatedField(models.ForeignKey):
    def formfield(self, **kwargs):
        return super().formfield(**kwargs)

class RelatedFieldTests:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_formfield_without_limit_choices_to(self):
        field = TestRelatedField(User, on_delete=models.CASCADE)
        form_field = field.formfield()
        assert isinstance(form_field, forms.ModelChoiceField)
        assert 'limit_choices_to' not in form_field.__dict__

    def test_formfield_with_limit_choices_to(self):
        field = TestRelatedField(User, on_delete=models.CASCADE)
        field.remote_field = type('RemoteField', (), {'limit_choices_to': Q(username='testuser')})()
        form_field = field.formfield()
        assert isinstance(form_field, forms.ModelChoiceField)
        assert form_field.limit_choices_to == Q(username='testuser')

    def test_formfield_with_additional_kwargs(self):
        field = TestRelatedField(User, on_delete=models.CASCADE)
        form_field = field.formfield(label='User', required=True)
        assert form_field.label == 'User'
        assert form_field.required is True

    def test_formfield_combined_limit_choices_to_and_additional_kwargs(self):
        field = TestRelatedField(User, on_delete=models.CASCADE)
        field.remote_field = type('RemoteField', (), {'limit_choices_to': Q(username='testuser')})()
        form_field = field.formfield(label='User', required=False)
        assert form_field.label == 'User'
        assert form_field.required is False
        assert form_field.limit_choices_to == Q(username='testuser')