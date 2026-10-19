import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms.models import ModelChoiceField

@pytest.mark.parametrize("value, expected", [
    (None, None),  # empty value
    (1, 1),        # valid primary key
    ("invalid", "invalid")  # invalid primary key
])
def test_to_python(value, expected):
    # Setup
    user1 = User.objects.create(username="user1")
    user2 = User.objects.create(username="user2")
    queryset = User.objects.all()
    
    # Instantiate ModelChoiceField with queryset
    field = ModelChoiceField(queryset=queryset)
    
    if value == "invalid":
        # Assert that ValidationError is raised for an invalid choice
        with pytest.raises(ValidationError):
            field.to_python(value)
    else:
        result = field.to_python(value)
        # Assert the correct value is returned
        assert result == (user1.pk if value == 1 else user2.pk if value == 2 else None)