import pytest
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def token_generator():
    return PasswordResetTokenGenerator()

def test_make_token_with_timestamp(token_generator, user):
    timestamp = int((datetime.now() - datetime(2001, 1, 1)).total_seconds())
    
    # Test with legacy as False
    token = token_generator._make_token_with_timestamp(user, timestamp, legacy=False)
    ts_b36, hash_string = token.split('-')
    assert len(ts_b36) == 6
    
    # Verify the hash structure
    assert constant_time_compare(token, token_generator._make_token_with_timestamp(user, timestamp, legacy=True)) != token

    # Test with legacy as True
    legacy_token = token_generator._make_token_with_timestamp(user, timestamp, legacy=True)
    assert legacy_token != token

    # Check if it is possible to recreate the token for the same user and timestamp
    recreated_token = token_generator._make_token_with_timestamp(user, timestamp, legacy=False)
    assert constant_time_compare(token, recreated_token)