import pytest
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TestPasswordResetTokenGenerator:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='password123')

    @pytest.fixture
    def token_generator(self):
        return PasswordResetTokenGenerator()

    def test_make_token_with_timestamp(self, user, token_generator):
        timestamp = int((datetime.now() - datetime(2001, 1, 1)).total_seconds())
        
        # Test without legacy flag
        token = token_generator._make_token_with_timestamp(user, timestamp, legacy=False)
        ts_b36, hash_string = token.split('-')
        assert len(ts_b36) == 6  # Base36 encoded timestamp
        assert constant_time_compare(token, token_generator._make_token_with_timestamp(user, timestamp, legacy=False))

        # Test with legacy flag
        legacy_token = token_generator._make_token_with_timestamp(user, timestamp, legacy=True)
        assert token != legacy_token  # Ensure tokens differ
        assert constant_time_compare(legacy_token, token_generator._make_token_with_timestamp(user, timestamp, legacy=True))

    def test_make_token_with_different_timestamps(self, user, token_generator):
        timestamp1 = int((datetime.now() - datetime(2001, 1, 1)).total_seconds())
        timestamp2 = timestamp1 + 1  # Different timestamp
        
        token1 = token_generator._make_token_with_timestamp(user, timestamp1, legacy=False)
        token2 = token_generator._make_token_with_timestamp(user, timestamp2, legacy=False)
        
        assert token1 != token2  # Ensure tokens are different for different timestamps