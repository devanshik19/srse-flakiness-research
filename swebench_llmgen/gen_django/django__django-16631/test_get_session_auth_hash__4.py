import pytest
from django.contrib.auth.models import User
from django.utils.crypto import salted_hmac

@pytest.mark.django_db
def test_get_session_auth_hash():
    # Create a user instance
    user = User.objects.create_user(username='testuser', password='testpassword')

    # Calculate the expected hash
    key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
    expected_hash = salted_hmac(key_salt, user.password, algorithm="sha256").hexdigest()

    # Call the method
    auth_hash = user.get_session_auth_hash()

    # Assert that the generated hash matches the expected hash
    assert auth_hash == expected_hash