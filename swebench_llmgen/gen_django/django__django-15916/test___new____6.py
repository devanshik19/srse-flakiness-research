import pytest
from django.core.exceptions import ImproperlyConfigured, FieldError, ValidationError
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db import models

class TestModelFormMetaclass:
    def test_new_method_with_valid_model(self):
        class Meta:
            model = User
            fields = '__all__'

        class ValidForm(ModelForm, metaclass=ModelFormMetaclass):
            Meta = Meta

        form = ValidForm()
        assert 'username' in form.fields
        assert 'password' in form.fields

    def test_new_method_without_fields_or_exclude(self):
        class Meta:
            model = User

        with pytest.raises(ImproperlyConfigured):
            class InvalidForm(ModelForm, metaclass=ModelFormMetaclass):
                Meta = Meta

    def test_new_method_with_string_fields(self):
        class Meta:
            model = User
            fields = 'username'  # Invalid format

        with pytest.raises(TypeError, match="cannot be a string"):
            class StringFieldForm(ModelForm, metaclass=ModelFormMetaclass):
                Meta = Meta

    def test_new_method_with_unknown_fields(self):
        class Meta:
            model = User
            fields = ['username', 'unknown_field']  # 'unknown_field' does not exist

        with pytest.raises(FieldError, match="Unknown field\(s\) \(unknown_field\) specified for User"):
            class UnknownFieldForm(ModelForm, metaclass=ModelFormMetaclass):
                Meta = Meta
            
    def test_new_method_overriding_fields(self):
        class Meta:
            model = User
            fields = ['username']

        class CustomForm(ModelForm, metaclass=ModelFormMetaclass):
            Meta = Meta
            declared_fields = {
                'custom_field': 'some_value',
            }

        form = CustomForm()
        assert 'username' in form.base_fields
        assert 'custom_field' in form.base_fields