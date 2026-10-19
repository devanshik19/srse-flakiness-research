import pytest
from django.core.exceptions import ImproperlyConfigured, FieldError
from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelFormMetaclass

class TestModelFormMetaclass:
    
    def test_new_with_no_fields_or_excludes(self):
        class TestForm(forms.ModelForm, metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                fields = None
        
        with pytest.raises(ImproperlyConfigured):
            TestForm()

    def test_new_with_invalid_fields_string(self):
        class TestForm(forms.ModelForm, metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                fields = 'username'
        
        with pytest.raises(TypeError) as excinfo:
            TestForm()
        assert "Did you mean to type: ('" in str(excinfo.value)

    def test_new_with_missing_fields(self):
        class TestForm(forms.ModelForm, metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                fields = ['first_name', 'last_name']  # Only if these are defined in User
        
        form = TestForm()
        assert 'first_name' in form.fields
        assert 'last_name' in form.fields

    def test_new_with_valid_configuration(self):
        class TestForm(forms.ModelForm, metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                fields = ['username']
        
        form = TestForm()
        assert 'username' in form.fields
        assert isinstance(form.fields['username'], forms.fields.CharField)

    def test_new_with_custom_fields(self):
        class TestForm(forms.ModelForm, metaclass=ModelFormMetaclass):
            custom_field = forms.CharField()

            class Meta:
                model = User
                fields = ['username']
        
        form = TestForm()
        assert 'username' in form.fields
        assert 'custom_field' in form.fields