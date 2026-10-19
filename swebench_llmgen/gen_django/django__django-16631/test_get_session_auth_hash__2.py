import pytest
from django.contrib.auth.models import User

@pytest.mark.parametrize("password", ["simplepassword", "Complex@1234", "123456"])
def test_get_session_auth_hash(password):
    user = User(username='testuser', password=password)
    user.set_password(password)  # Set the password using Django's method
    user.save()  # Save the user to the database

    expected_hash = user.get_session_auth_hash()
    actual_hash = salted_hmac(
        "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash",
        user.password,
        algorithm="sha256",
    ).hexdigest()

    assert expected_hash == actual_hash