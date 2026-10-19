import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms.models import ModelChoiceField

@pytest.mark.django_db
class TestModelChoiceField:
    def setup_method(self):
        # Creating a sample queryset with User objects
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.field = ModelChoiceField(queryset=User.objects.all())

    def test_to_python_valid_instance(self):
        result = self.field.to_python(self.user1)
        assert result == self.user1.pk

    def test_to_python_valid_pk(self):
        result = self.field.to_python(self.user2.pk)
        assert result == self.user2.pk

    def test_to_python_invalid_value_not_in_queryset(self):
        with pytest.raises(ValidationError):
            self.field.to_python(999)  # a non-existent User PK

    def test_to_python_invalid_type_value(self):
        with pytest.raises(ValidationError):
            self.field.to_python("invalid_string")  # invalid type

    def test_to_python_empty_value(self):
        result = self.field.to_python(None)
        assert result is None