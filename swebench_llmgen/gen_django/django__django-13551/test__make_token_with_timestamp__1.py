import pytest
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

@pytest.mark.parametrize("legacy,expected_length", [
    (False, 43),  # 6 base36 digits + 32 hex digits for sha1
    (True, 43),   # similarly for legacy sha1
])
def test_make_token_with_timestamp(legacy, expected_length):
    user = User.objects.create_user(username='testuser', password='testpass')
    timestamp = int((datetime.now() - datetime(2001, 1, 1)).total_seconds())
    
    token_generator = PasswordResetTokenGenerator()
    token_generator.key_salt = 'django.contrib.auth.models.User'
    token_generator.secret = 'my_secret'
    token_generator.algorithm = 'sha1'
    
    token = token_generator._make_token_with_timestamp(user, timestamp, legacy)

    assert isinstance(token, str)
    assert len(token) == expected_length
    assert '-' in token
    ts_b36, hash_string = token.split('-')
    assert len(ts_b36) == 6
    assert all(c in "0123456789abcdefghijklmnopqrstuvwxyz" for c in ts_b36)
    assert len(hash_string) == 32  # Length of the hex digest should be 32
    assert all(c in "0123456789abcdef" for c in hash_string)