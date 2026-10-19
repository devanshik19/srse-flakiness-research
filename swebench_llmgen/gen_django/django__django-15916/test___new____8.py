import pytest
from django.core.exceptions import ImproperlyConfigured, FieldError
from django.forms import ModelForm
from django.contrib.auth.models import User

class TestModelFormMetaclass:
    
    def test_new_with_valid_fields(self):
        class UserForm(ModelForm, metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                fields = ['username', 'email']

        assert hasattr(UserForm, 'base_fields')
        assert 'username' in UserForm.base_fields
        assert 'email' in UserForm.base_fields

    def test_new_with_exclude(self):
        class UserForm(ModelForm, metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                exclude = ['date_joined']

        assert hasattr(UserForm, 'base_fields')
        assert 'date_joined' not in UserForm.base_fields

    def test_new_without_fields_or_exclude(self):
        with pytest.raises(ImproperlyConfigured):
            class UserForm(ModelForm, metaclass=ModelFormMetaclass):
                class Meta:
                    model = User

    def test_new_with_string_fields(self):
        with pytest.raises(TypeError) as excinfo:
            class UserForm(ModelForm, metaclass=ModelFormMetaclass):
                class Meta:
                    model = User
                    fields = 'username'

        assert "Meta.fields cannot be a string." in str(excinfo.value)

    def test_new_with_invalid_field(self):
        with pytest.raises(FieldError) as excinfo:
            class UserForm(ModelForm, metaclass=ModelFormMetaclass):
                class Meta:
                    model = User
                    fields = ['non_existing_field']

        assert "Unknown field(s) (non_existing_field) specified for User" in str(excinfo.value)