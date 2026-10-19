import hashlib
import pytest
from django.contrib.auth.models import User
from django.utils.crypto import salted_hmac


@pytest.mark.parametrize("password", ["password123", "securepassword!", "p@ssw0rd"])
def test_get_session_auth_hash(password):
    user = User(username="testuser", password=password)
    user.set_password(password)
    user.save()
    expected_key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
    expected_hash = salted_hmac(expected_key_salt, user.password, algorithm="sha256").hexdigest()
    
    assert expected_hash == user.get_session_auth_hash()
    
def test_get_session_auth_hash_no_password():
    user = User(username="testuser_no_pass")
    user.save()
    expected_key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
    expected_hash = salted_hmac(expected_key_salt, "", algorithm="sha256").hexdigest()
    
    assert expected_hash == user.get_session_auth_hash()