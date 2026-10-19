import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict

@pytest.mark.parametrize("fields, exclude, expected", [
    (None, None, {"username": "testuser", "email": "testuser@example.com"}),
    (["username"], None, {"username": "testuser"}),
    (None, ["email"], {"username": "testuser"}),
    (["username", "email"], ["email"], {"username": "testuser"}),
])
def test_model_to_dict(fields, exclude, expected):
    user = User(username="testuser", email="testuser@example.com")
    user.save()
    result = model_to_dict(user, fields=fields, exclude=exclude)
    assert result == expected

def test_model_to_dict_with_non_editable_field():
    user = User(username="testuser", email="testuser@example.com")
    user.save()
    result = model_to_dict(user, exclude=['last_login'])
    assert 'last_login' not in result

def test_model_to_dict_empty_fields():
    user = User(username="testuser", email="testuser@example.com")
    user.save()
    result = model_to_dict(user, fields=[])
    assert result == {}