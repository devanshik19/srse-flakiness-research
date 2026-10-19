import pytest
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

@pytest.mark.parametrize("fields, exclude, expected", [
    (None, None, {"username": "testuser", "email": "test@example.com", "first_name": "", "last_name": ""}),
    (["username", "email"], None, {"username": "testuser", "email": "test@example.com"}),
    (None, ["username"], {"email": "test@example.com", "first_name": "", "last_name": ""}),
    (["username", "first_name"], ["first_name"], {"username": "testuser"})
])
def test_model_to_dict(fields, exclude, expected):
    user = User(username="testuser", email="test@example.com")
    user.save()
    
    result = model_to_dict(user, fields=fields, exclude=exclude)
    
    assert result == expected