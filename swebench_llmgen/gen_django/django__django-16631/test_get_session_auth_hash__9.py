import pytest
from django.contrib.auth.models import User
from django.utils.crypto import salted_hmac

@pytest.mark.parametrize("password, expected_hash", [
    ("password123", salted_hmac("django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash", "password123", algorithm="sha256").hexdigest()),
    ("123456", salted_hmac("django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash", "123456", algorithm="sha256").hexdigest()),
])
def test_get_session_auth_hash(password, expected_hash):
    user = User(username='testuser', password=password)
    user.set_password(password)
    user.save()

    assert user.get_session_auth_hash() == expected_hash