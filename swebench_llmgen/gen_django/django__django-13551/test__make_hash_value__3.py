import pytest
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime

@pytest.mark.django_db
def test_make_hash_value():
    # Setup
    user = User.objects.create_user(username='testuser', password='password123')
    user.last_login = datetime(2023, 1, 1, 12, 0, 0)
    user.save()

    timestamp = int(datetime.now().timestamp())
    token_generator = PasswordResetTokenGenerator()

    # Expected hash value computation
    expected_hash_value = str(user.pk) + user.password + str(user.last_login.replace(microsecond=0, tzinfo=None)) + str(timestamp)
    
    # Test the _make_hash_value method
    hash_value = token_generator._make_hash_value(user, timestamp)
    
    assert hash_value == expected_hash_value

    # Test with last_login set to None
    user.last_login = None
    user.save()

    expected_hash_value_none_login = str(user.pk) + user.password + '' + str(timestamp)
    
    hash_value_none_login = token_generator._make_hash_value(user, timestamp)
    
    assert hash_value_none_login == expected_hash_value_none_login