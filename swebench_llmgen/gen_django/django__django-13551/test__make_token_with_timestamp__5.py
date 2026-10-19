import pytest
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator


@pytest.mark.parametrize("legacy, expected_length", [(False, 43), (True, 43)])
def test_make_token_with_timestamp(legacy, expected_length):
    user = User.objects.create(username="testuser", email="test@example.com")
    token_generator = PasswordResetTokenGenerator()
    
    timestamp = int((datetime.now() - datetime(2001, 1, 1)).total_seconds())
    token = token_generator._make_token_with_timestamp(user, timestamp, legacy)

    # Ensure the token has the expected length
    assert len(token) == expected_length

    # Ensure the token has the correct format of "base36-timestamp-hash"
    ts_b36, hash_string = token.split('-')
    assert len(ts_b36) == 6  # Base36 representation should be 6 characters
    assert len(hash_string) == 20  # The hash length should be consistent
    
    # Test hash functionality (optional)
    assert token_generator.secret is not None
    assert token_generator.key_salt is not None
    assert token_generator.algorithm is not None