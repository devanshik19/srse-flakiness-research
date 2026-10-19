import pytest
from django.core.exceptions import ImproperlyConfigured, FieldError, TypeError
from django.forms import ModelForm
from django.contrib.auth.models import User

class TestModelFormMetaclass:
    
    def test_new_method_without_fields_or_exclude(self):
        class Meta:
            model = User
        
        with pytest.raises(ImproperlyConfigured, match="needs updating"):
            class TestForm(ModelForm, metaclass=ModelFormMetaclass):
                class Meta(Meta):
                    pass

    def test_new_method_with_string_fields(self):
        class Meta:
            model = User
            fields = 'username'

        with pytest.raises(TypeError, match="cannot be a string"):
            class TestForm(ModelForm, metaclass=ModelFormMetaclass):
                class Meta(Meta):
                    pass

    def test_new_method_with_invalid_field(self):
        class Meta:
            model = User
            fields = ['non_existing_field']

        with pytest.raises(FieldError, match="Unknown field"):
            class TestForm(ModelForm, metaclass=ModelFormMetaclass):
                class Meta(Meta):
                    pass

    def test_new_method_with_valid_fields(self):
        class Meta:
            model = User
            fields = ['username', 'email']

        class TestForm(ModelForm, metaclass=ModelFormMetaclass):
            class Meta(Meta):
                pass

        form = TestForm()
        assert 'username' in form.base_fields
        assert 'email' in form.base_fields