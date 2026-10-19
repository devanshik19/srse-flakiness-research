import pytest
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

@pytest.mark.parametrize(
    "timestamp, legacy, expected_length",
    [
        (int((datetime(2021, 1, 1) - datetime(2001, 1, 1)).total_seconds()), False, 28),
        (int((datetime(2023, 1, 1) - datetime(2001, 1, 1)).total_seconds()), False, 28),
        (int((datetime(2024, 1, 1) - datetime(2001, 1, 1)).total_seconds()), True, 28),
    ]
)
def test_make_token_with_timestamp(timestamp, legacy, expected_length):
    user = User.objects.create_user(username='testuser', password='testpass')
    token_generator = PasswordResetTokenGenerator()
    token_generator.key_salt = "django.contrib.auth.tokens"
    token_generator.secret = "my_secret"
    token_generator.algorithm = "sha256"

    token = token_generator._make_token_with_timestamp(user, timestamp, legacy)
    
    assert isinstance(token, str)
    assert len(token) == expected_length
    assert '-' in token