import pytest
from django.core.exceptions import ValidationError
from django.db.models.fields import Field

class CustomField(Field):
    def to_python(self, value):
        if value in self.empty_values:
            return None
        if isinstance(value, str) and value.isdigit():
            return int(value)
        raise ValidationError("Invalid value")

def test_to_python():
    field = CustomField()
    
    # Test handling of empty values
    for empty_value in field.empty_values:
        assert field.to_python(empty_value) is None
    
    # Test valid string integer conversion
    assert field.to_python("123") == 123
    assert field.to_python("0") == 0

    # Test invalid inputs
    with pytest.raises(ValidationError):
        field.to_python("abc")
    
    with pytest.raises(ValidationError):
        field.to_python("123.45")
    
    with pytest.raises(ValidationError):
        field.to_python(None)