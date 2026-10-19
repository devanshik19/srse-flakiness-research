import pytest
from django.core.exceptions import ImproperlyConfigured, FieldError
from django.forms import ModelForm
from django.contrib.auth.models import User

class TestModelFormMetaclass:

    def test_new_method_with_valid_fields(self):
        class TestForm(ModelForm, metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                fields = ['username', 'email']
        
        assert hasattr(TestForm.base_fields, 'username')
        assert hasattr(TestForm.base_fields, 'email')

    def test_new_method_without_fields_or_exclude(self):
        with pytest.raises(ImproperlyConfigured):
            class TestForm(ModelForm, metaclass=ModelFormMetaclass):
                class Meta:
                    model = User
        
    def test_new_method_with_string_fields(self):
        with pytest.raises(TypeError) as excinfo:
            class TestForm(ModelForm, metaclass=ModelFormMetaclass):
                class Meta:
                    model = User
                    fields = 'username'
        
        assert "Must be a tuple" in str(excinfo.value)

    def test_new_method_with_unknown_field(self):
        with pytest.raises(FieldError) as excinfo:
            class TestForm(ModelForm, metaclass=ModelFormMetaclass):
                class Meta:
                    model = User
                    fields = ['unknown_field']
        
        assert "Unknown field(s)" in str(excinfo.value)