import pytest
from django.contrib.auth.models import User
from django.utils.crypto import salted_hmac

@pytest.mark.parametrize("password", ["password123", "123456", "mypassword", "anotherpassword"])
def test_get_session_auth_hash(password):
    # Create a User instance and set the password
    user = User(username="testuser", password=password)
    user.set_password(password)  # Set the password using the User's method
    user.save()  # Save the user to the database to ensure the password is hashed

    # Manually retrieve the password to verify the session auth hash
    key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
    expected_hash = salted_hmac(key_salt, password).hexdigest()

    # Call the method and check that the output matches the expected hash
    assert user.get_session_auth_hash() == expected_hash