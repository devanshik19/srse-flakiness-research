import pytest
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime

@pytest.mark.django_db
def test_make_token_with_timestamp():
    user = User.objects.create_user(username='testuser', password='password123')
    
    generator = PasswordResetTokenGenerator()
    timestamp = int((datetime(2022, 1, 1) - datetime(2001, 1, 1)).total_seconds())
    
    # Test without legacy flag
    token = generator._make_token_with_timestamp(user, timestamp, legacy=False)
    
    assert isinstance(token, str)
    assert len(token.split('-')) == 2  # Check that token consists of two parts
    
    ts_b36, hash_string = token.split('-')
    assert len(ts_b36) == 6  # Base36 timestamp should have length 6
    assert all(c in '0123456789abcdefghijklmnopqrstuvwxyz' for c in ts_b36)  # Check valid base36
    
    # Test with legacy flag
    legacy_token = generator._make_token_with_timestamp(user, timestamp, legacy=True)
    
    assert isinstance(legacy_token, str)
    assert legacy_token != token  # Ensure legacy token is different from the non-legacy token