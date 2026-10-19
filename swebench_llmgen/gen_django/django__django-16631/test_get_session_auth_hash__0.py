import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_get_session_auth_hash():
    # Create a user instance
    user = User(username='testuser', password='testpassword')
    user.set_password('testpassword')  # Ensures the password is hashed
    user.save()

    # Calculate the expected HMAC
    key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
    expected_hash = salted_hmac(
        key_salt,
        user.password,
        algorithm="sha256",
    ).hexdigest()

    # Call the get_session_auth_hash method
    session_auth_hash = user.get_session_auth_hash()

    # Assert the returned hash matches the expected hash
    assert session_auth_hash == expected_hash