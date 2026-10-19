import pytest
from django.core.exceptions import ImproperlyConfigured, FieldError
from django.forms import ModelForm
from django.forms.models import ModelFormMetaclass
from django.contrib.auth.models import User

class TestModelFormMetaclass:

    class Meta:
        model = User
        fields = ['username', 'email']

    def test_new_with_valid_fields(self):
        class ValidModelForm(metaclass=ModelFormMetaclass):
            Meta = self.Meta

        form = ValidModelForm()
        assert set(form.base_fields.keys()) == {'username', 'email'}

    def test_new_without_fields_or_exclude(self):
        class InvalidModelForm(metaclass=ModelFormMetaclass):
            class Meta:
                model = User

        with pytest.raises(ImproperlyConfigured) as excinfo:
            InvalidModelForm()
        assert "needs updating" in str(excinfo.value)

    def test_new_with_string_fields(self):
        class StringFieldModelForm(metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                fields = 'username'

        with pytest.raises(TypeError) as excinfo:
            StringFieldModelForm()
        assert "cannot be a string" in str(excinfo.value)

    def test_new_with_missing_fields(self):
        class MissingFieldModelForm(metaclass=ModelFormMetaclass):
            class Meta:
                model = User
                fields = ['non_existing_field']

        with pytest.raises(FieldError) as excinfo:
            MissingFieldModelForm()
        assert "Unknown field(s)" in str(excinfo.value)