import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Field


class TestField(Field):

    def to_python(self, value):
        """
        Convert the input value into the expected Python data type, raising
        django.core.exceptions.ValidationError if the data can't be converted.
        Return the converted value. Subclasses should override this.
        """
        if not isinstance(value, (str, int, float, bool, type(None))):
            raise ValidationError("Invalid value type")
        return value


def test_to_python_with_valid_values():
    test_field = TestField()

    # Test with valid values
    assert test_field.to_python("test string") == "test string"
    assert test_field.to_python(123) == 123
    assert test_field.to_python(45.67) == 45.67
    assert test_field.to_python(True) is True
    assert test_field.to_python(False) is False
    assert test_field.to_python(None) is None


def test_to_python_with_invalid_value():
    test_field = TestField()

    # Test with invalid value type
    with pytest.raises(ValidationError, match="Invalid value type"):
        test_field.to_python([1, 2, 3])  # List
    with pytest.raises(ValidationError, match="Invalid value type"):
        test_field.to_python({"key": "value"})  # Dictionary
    with pytest.raises(ValidationError, match="Invalid value type"):
        test_field.to_python(uuid.uuid4())  # UUID
    with pytest.raises(ValidationError, match="Invalid value type"):
        test_field.to_python(object())  # Custom object


def test_to_python_with_user_instance():
    test_field = TestField()

    # Testing with an instance of User model
    user_instance = User(username='testuser', password='testpass')
    user_instance.full_clean()

    assert test_field.to_python(user_instance) == user_instance