import pytest
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

@pytest.mark.parametrize("legacy", [True, False])
def test_make_token_with_timestamp(legacy):
    # Arrange
    user = User.objects.create_user(username='testuser', password='testpass')
    timestamp = int((datetime.now() - datetime(2001, 1, 1)).total_seconds())
    token_generator = PasswordResetTokenGenerator()
    
    # Act
    token = token_generator._make_token_with_timestamp(user, timestamp, legacy)

    # Assert
    assert isinstance(token, str)
    assert len(token.split('-')) == 2  # Ensure it has two parts (timestamp, hash)
    ts_b36, hash_string = token.split('-')
    assert len(ts_b36) == 6  # Base 36 representation of the timestamp
    assert len(hash_string) > 0  # Ensure the hash part is non-empty

    # Check the content of the token follows the expected format
    assert token == f"{ts_b36}-{token_generator.secret[:10]}"

    # Test the token can be generated with legacy flag
    legacy_token = token_generator._make_token_with_timestamp(user, timestamp, legacy=True)
    assert token != legacy_token  # Tokens should differ based on legacy flag