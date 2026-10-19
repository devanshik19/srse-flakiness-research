import pytest
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone

@pytest.mark.parametrize("last_login, expected_hash", [
    (None, "1password1234567890"),  # When last_login is None
    (timezone.now(), "1password1234567890"),  # With a current last_login timestamp
])
def test_make_hash_value(last_login, expected_hash):
    user = User(pk=1, password="password", last_login=last_login)
    timestamp = 1234567890
    token_generator = PasswordResetTokenGenerator()

    # Set the user's last_login before using the token generator
    user.last_login = last_login
    assert token_generator._make_hash_value(user, timestamp) == str(user.pk) + user.password + ('' if not last_login else str(last_login.replace(microsecond=0, tzinfo=None))) + str(timestamp)

def test_make_hash_value_with_different_user_fields():
    user1 = User(pk=1, password="password1", last_login=timezone.now())
    user2 = User(pk=2, password="password2", last_login=timezone.now())
    timestamp = 1234567890
    token_generator = PasswordResetTokenGenerator()

    hash_value1 = token_generator._make_hash_value(user1, timestamp)
    hash_value2 = token_generator._make_hash_value(user2, timestamp)
    
    assert hash_value1 != hash_value2  # Ensure different users produce different hash values