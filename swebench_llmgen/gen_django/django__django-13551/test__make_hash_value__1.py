import pytest
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

@pytest.mark.parametrize("last_login,expected_login_timestamp", [
    (None, ''),  # Case with no last login
    (datetime(2023, 1, 1, 12, 0, 0), '2023-01-01 12:00:00'),  # Valid last login
])
def test_make_hash_value(last_login, expected_login_timestamp):
    # Arrange
    user = User(pk=1, password='hashed_password', last_login=last_login)
    timestamp = 1234567890  # Sample timestamp
    token_generator = PasswordResetTokenGenerator()

    # Act
    hash_value = token_generator._make_hash_value(user, timestamp)

    # Assert
    expected_hash_value = f"1hashed_password{expected_login_timestamp}1234567890"
    assert hash_value == expected_hash_value