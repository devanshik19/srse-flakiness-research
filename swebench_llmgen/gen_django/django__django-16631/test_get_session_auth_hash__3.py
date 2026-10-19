import pytest
from django.contrib.auth.models import User
from django.utils.crypto import salted_hmac

@pytest.mark.django_db
def test_get_session_auth_hash():
    user = User.objects.create_user(username='testuser', password='securepassword')
    
    key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
    expected_hash = salted_hmac(key_salt, user.password, algorithm="sha256").hexdigest()

    assert user.get_session_auth_hash() == expected_hash

    # Testing with a different password
    user.set_password('newpassword')
    user.save()

    new_expected_hash = salted_hmac(key_salt, user.password, algorithm="sha256").hexdigest()
    assert user.get_session_auth_hash() == new_expected_hash

    # Ensure it doesn't match the old hash
    assert user.get_session_auth_hash() != expected_hash