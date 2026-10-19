import pytest
from django.forms import ModelForm
from django.core.exceptions import ImproperlyConfigured, TypeError, FieldError
from django.contrib.auth.models import User

class TestModelFormMetaclass:

    class Meta:
        model = User
        fields = ('username', 'email')

    def test_new_method_with_valid_fields(self):
        class UserForm(ModelForm, metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                fields = ['username', 'email']

        form = UserForm()
        assert set(form.base_fields.keys()) == {'username', 'email'}

    def test_new_method_with_missing_fields(self):
        with pytest.raises(ImproperlyConfigured):
            class UserForm(ModelForm, metaclass=ModelFormMetaclass):
                class Meta:
                    model = User

    def test_new_method_with_string_fields(self):
        with pytest.raises(TypeError):
            class UserForm(ModelForm, metaclass=ModelFormMetaclass):
                class Meta:
                    model = User
                    fields = 'username'

    def test_new_method_with_invalid_field(self):
        with pytest.raises(FieldError):
            class UserForm(ModelForm, metaclass=ModelFormMetaclass):
                class Meta:
                    model = User
                    fields = ['username', 'non_existing_field']