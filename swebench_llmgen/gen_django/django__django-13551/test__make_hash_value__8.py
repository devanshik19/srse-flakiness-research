import pytest
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime

@pytest.mark.parametrize("last_login, expected_hash_value", [
    (None, lambda timestamp: f"{1}password{''}{timestamp}"),
    (datetime(2023, 1, 1, 12, 0, 0), lambda timestamp: f"{1}password{datetime(2023, 1, 1, 12, 0).strftime('%Y-%m-%d %H:%M:%S')}{timestamp}"),
])
def test_make_hash_value(last_login, expected_hash_value):
    user = User(pk=1, password='password', last_login=last_login)
    timestamp = 1234567890
    generator = PasswordResetTokenGenerator()

    if callable(expected_hash_value):
        expected_result = expected_hash_value(timestamp)
    else:
        expected_result = expected_hash_value

    result = generator._make_hash_value(user, timestamp)
    
    assert result == expected_result