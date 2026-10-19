import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms.models import ModelChoiceField

class TestModelChoiceField:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.field = ModelChoiceField(queryset=User.objects.all())
    
    def test_to_python_with_valid_instance(self):
        result = self.field.to_python(self.user)
        assert result == self.user.pk

    def test_to_python_with_valid_primary_key(self):
        result = self.field.to_python(self.user.pk)
        assert result == self.user.pk

    def test_to_python_with_empty_value(self):
        result = self.field.to_python('')
        assert result is None

    def test_to_python_with_invalid_primary_key(self):
        with pytest.raises(ValidationError) as excinfo:
            self.field.to_python(999)  # Assuming 999 does not exist
        assert str(excinfo.value) == self.field.error_messages['invalid_choice']

    def test_to_python_with_none(self):
        result = self.field.to_python(None)
        assert result is None