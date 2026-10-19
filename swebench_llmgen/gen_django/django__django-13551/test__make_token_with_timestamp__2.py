import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TestPasswordResetTokenGenerator:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='testpassword')

    @pytest.fixture
    def token_generator(self):
        return PasswordResetTokenGenerator()

    def test_make_token_with_timestamp(self, token_generator, user):
        timestamp = int((timezone.now() - timezone.datetime(2001, 1, 1)).total_seconds())
        
        # Call the method with legacy set to False
        token = token_generator._make_token_with_timestamp(user, timestamp, legacy=False)
        assert isinstance(token, str)
        assert len(token.split('-')) == 2  # Ensure it has two parts

        # Call with legacy set to True
        legacy_token = token_generator._make_token_with_timestamp(user, timestamp, legacy=True)
        assert isinstance(legacy_token, str)
        assert len(legacy_token.split('-')) == 2  # Ensure it has two parts

        # Ensure that the two tokens differ
        assert token != legacy_token
        
        # Ensure the timestamp part is a valid base 36 encoding
        ts_b36 = token.split('-')[0]
        assert len(ts_b36) > 0
        assert all(c.isalnum() for c in ts_b36)

        # Test with a different timestamp
        timestamp2 = timestamp + 10000
        token2 = token_generator._make_token_with_timestamp(user, timestamp2, legacy=False)
        assert token != token2  # Different timestamp should produce a different token