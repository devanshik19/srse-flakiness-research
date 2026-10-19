import pytest
from django.core.exceptions import ImproperlyConfigured, FieldError
from django.forms import ModelForm
from django.contrib.auth.models import User

class Meta:
    model = User
    fields = ['username', 'password']

class UserForm(ModelForm, metaclass=ModelFormMetaclass):
    class Meta(Meta):
        pass

def test_model_form_metaclass_new_without_fields_or_exclude():
    with pytest.raises(ImproperlyConfigured) as excinfo:
        class InvalidUserForm(ModelForm, metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                fields = None
                exclude = None
    
    assert "needs updating" in str(excinfo.value)

def test_model_form_metaclass_new_with_invalid_field():
    with pytest.raises(FieldError) as excinfo:
        class InvalidFieldUserForm(ModelForm, metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                fields = ['invalid_field']
    
    assert "Unknown field(s) (invalid_field) specified" in str(excinfo.value)

def test_model_form_metaclass_new_with_correct_fields():
    class ValidUserForm(ModelForm, metaclass=ModelFormMetaclass):
        class Meta:
            model = User
            fields = ['username']
    
    form = ValidUserForm()
    assert 'username' in form.base_fields
    assert len(form.base_fields) == 1

def test_model_form_metaclass_new_with_fields_as_string():
    with pytest.raises(TypeError) as excinfo:
        class StringFieldsUserForm(ModelForm, metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                fields = 'username'
    
    assert "Did you mean to type: ('username',)?" in str(excinfo.value)