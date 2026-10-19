import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms import ModelChoiceField

class TestModelChoiceField:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        # Create some test user instances
        self.user1 = User.objects.create(username='testuser1')
        self.user2 = User.objects.create(username='testuser2')
        self.user3 = User.objects.create(username='testuser3')

        # Create a ModelChoiceField with the User queryset
        self.choice_field = ModelChoiceField(queryset=User.objects.all())

    def test_to_python_valid_choice(self):
        # Test with a valid user ID
        assert self.choice_field.to_python(self.user1.pk) == self.user1

    def test_to_python_valid_instance(self):
        # Test with a valid user instance
        assert self.choice_field.to_python(self.user2) == self.user2

    def test_to_python_invalid_choice(self):
        # Test with a non-existent user ID
        with pytest.raises(ValidationError) as excinfo:
            self.choice_field.to_python(999)
        assert str(excinfo.value) == str(self.choice_field.error_messages['invalid_choice'])

    def test_to_python_empty_value(self):
        # Test with an empty value
        assert self.choice_field.to_python(None) is None
        assert self.choice_field.to_python('') is None