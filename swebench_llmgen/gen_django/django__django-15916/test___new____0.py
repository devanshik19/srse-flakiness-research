import pytest
from django.core.exceptions import ImproperlyConfigured, FieldError, TypeError
from django.forms import ModelForm
from django.contrib.auth.models import User


class TestModelFormMetaclass:
    
    class Meta:
        model = User
        fields = ['id']

    def test_modelform_metaclass_with_valid_fields(self):
        class UserForm(ModelForm, metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                fields = ['username', 'password']
        
        assert UserForm.base_fields['username'] is not None
        assert UserForm.base_fields['password'] is not None

    def test_modelform_metaclass_without_fields_or_excludes(self):
        with pytest.raises(ImproperlyConfigured, match=r"Creating a ModelForm without either the 'fields' attribute or the 'exclude' attribute is prohibited"):
            class InvalidUserForm(ModelForm, metaclass=ModelFormMetaclass):
                class Meta:
                    model = User
            
            InvalidUserForm()

    def test_modelform_metaclass_with_string_fields(self):
        with pytest.raises(TypeError, match=r"UserForm.Meta.fields cannot be a string. Did you mean to type: \('foo',\)\?"):
            class StringFieldUserForm(ModelForm, metaclass=ModelFormMetaclass):
                class Meta:
                    model = User
                    fields = 'username'

            StringFieldUserForm()

    def test_modelform_metaclass_with_invalid_field(self):
        with pytest.raises(FieldError, match=r"Unknown field\(s\) \(nonexistent_field\) specified for User"):
            class InvalidFieldUserForm(ModelForm, metaclass=ModelFormMetaclass):
                class Meta:
                    model = User
                    fields = ['username', 'nonexistent_field']
            
            InvalidFieldUserForm()