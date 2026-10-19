import pytest
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TestPasswordResetTokenGenerator:
    def setup_method(self):
        self.generator = PasswordResetTokenGenerator()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.timestamp = int((datetime.now() - datetime(2001, 1, 1)).total_seconds())

    def test_make_token_with_timestamp(self):
        token = self.generator._make_token_with_timestamp(self.user, self.timestamp, legacy=False)
        assert isinstance(token, str)
        assert len(token.split('-')) == 2

    def test_make_token_with_timestamp_legacy(self):
        token = self.generator._make_token_with_timestamp(self.user, self.timestamp, legacy=True)
        assert isinstance(token, str)
        assert len(token.split('-')) == 2

    def test_make_token_with_timestamp_format(self):
        token = self.generator._make_token_with_timestamp(self.user, self.timestamp, legacy=False)
        ts_b36, _ = token.split('-')
        assert len(ts_b36) == 6  # Base 36 timestamp should be 6 characters long

    def test_make_token_with_timestamp_different_user(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        token = self.generator._make_token_with_timestamp(other_user, self.timestamp, legacy=False)
        assert token != self.generator._make_token_with_timestamp(self.user, self.timestamp, legacy=False)

    def test_make_token_with_different_timestamps(self):
        future_timestamp = int((datetime.now() - datetime(2001, 1, 1)).total_seconds()) + 10000
        token_future = self.generator._make_token_with_timestamp(self.user, future_timestamp, legacy=False)
        token_current = self.generator._make_token_with_timestamp(self.user, self.timestamp, legacy=False)
        assert token_future != token_current