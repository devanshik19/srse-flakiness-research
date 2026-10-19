import pytest
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime

@pytest.mark.parametrize("last_login, expected_suffix", [
    (None, ""),  # Last login is None
    (datetime(2021, 1, 1, 12, 0, 0), "2021-01-01 12:00:00"),  # Last login with specific time
])
def test_make_hash_value(last_login, expected_suffix):
    # Arrange
    user = User.objects.create_user(username='testuser', password='testpassword')
    user.last_login = last_login
    user.save()
    
    timestamp = 1234567890  # Sample timestamp
    token_generator = PasswordResetTokenGenerator()

    # Act
    hash_value = token_generator._make_hash_value(user, timestamp)

    # Assert
    assert str(user.pk) in hash_value
    assert user.password in hash_value
    assert str(timestamp) in hash_value
    if last_login is None:
        assert expected_suffix not in hash_value  # Check the absence of last login info
    else:
        assert expected_suffix in hash_value  # Check for the last login timestamp presence