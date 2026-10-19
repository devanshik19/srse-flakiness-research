import pytest
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

@pytest.mark.parametrize("legacy", [True, False])
def test_make_token_with_timestamp(legacy):
    # Arrange
    user = User.objects.create_user(username='testuser', password='testpass')
    generator = PasswordResetTokenGenerator()
    timestamp = int((datetime(2023, 1, 1) - datetime(2001, 1, 1)).total_seconds())

    # Act
    token = generator._make_token_with_timestamp(user, timestamp, legacy)

    # Assert
    assert isinstance(token, str)
    assert len(token) > 0
    assert '-' in token
    ts_b36, hash_string = token.split('-')
    assert len(ts_b36) == 6  # Base 36 encoding should give 6 characters
    assert len(hash_string) > 0