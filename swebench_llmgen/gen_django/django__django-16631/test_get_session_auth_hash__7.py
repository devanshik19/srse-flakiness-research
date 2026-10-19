import pytest
from django.contrib.auth.models import User
from django.utils.crypto import salted_hmac

@pytest.mark.parametrize(
    "password, expected_hash",
    [
        ("test_password", salted_hmac("django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash", "test_password", algorithm="sha256").hexdigest()),
        ("another_password", salted_hmac("django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash", "another_password", algorithm="sha256").hexdigest()),
    ]
)
def test_get_session_auth_hash(password, expected_hash):
    user = User(username="testuser", password=password)
    user.set_password(password)  # Ensure the password is hashed
    user.save()
    
    assert user.get_session_auth_hash() == expected_hash