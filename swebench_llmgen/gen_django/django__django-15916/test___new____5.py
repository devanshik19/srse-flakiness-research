import pytest
from django.core.exceptions import ImproperlyConfigured, FieldError
from django.forms import ModelForm
from django.contrib.auth.models import User


class TestModelFormMetaclass:

    def test_new_class_no_model(self):
        class MyForm(metaclass=ModelFormMetaclass):
            class Meta:
                fields = ['username']

        with pytest.raises(ImproperlyConfigured):
            MyForm()

    def test_new_class_with_fields(self):
        class MyForm(metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                fields = ['username']

        form = MyForm()
        assert set(form.base_fields.keys()) == {'username'}

    def test_new_class_with_exclude(self):
        class MyForm(metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                exclude = ['password']

        form = MyForm()
        assert 'password' not in form.base_fields

    def test_new_class_with_invalid_field_string(self):
        class MyForm(metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                fields = 'username'

        with pytest.raises(TypeError) as exc_info:
            MyForm()
        assert "did you mean to type: ('username',)?" in str(exc_info.value)

    def test_new_class_with_missing_field(self):
        class MyForm(metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                fields = ['non_existent_field']

        with pytest.raises(FieldError) as exc_info:
            MyForm()
        assert "Unknown field(s) (non_existent_field) specified for User" in str(exc_info.value)