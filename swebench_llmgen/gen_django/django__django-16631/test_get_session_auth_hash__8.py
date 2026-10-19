import pytest
from django.contrib.auth.models import User
from django.utils.crypto import salted_hmac

@pytest.mark.django_db
def test_get_session_auth_hash():
    # Create a user instance
    user = User.objects.create_user(username='testuser', password='password123')

    # Calculate expected hash
    key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
    expected_hash = salted_hmac(key_salt, user.password, algorithm="sha256").hexdigest()

    # Assert that get_session_auth_hash returns the expected value
    assert user.get_session_auth_hash() == expected_hash

    # Change user's password to test different output
    user.set_password('newpassword456')
    
    # Calculate new expected hash
    expected_new_hash = salted_hmac(key_salt, user.password, algorithm="sha256").hexdigest()

    # Assert that the hash is now different
    assert user.get_session_auth_hash() == expected_new_hash