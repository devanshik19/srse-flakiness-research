import pytest
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')

def test_make_hash_value(user):
    # Arrange
    generator = PasswordResetTokenGenerator()
    timestamp = int(datetime.now().timestamp())

    # Act
    hash_value = generator._make_hash_value(user, timestamp)

    # Assert
    login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
    expected_hash_value = f"{user.pk}{user.password}{login_timestamp}{timestamp}"
    
    assert hash_value == expected_hash_value

def test_make_hash_value_with_last_login(user):
    # Arrange
    generator = PasswordResetTokenGenerator()
    user.last_login = datetime.now()
    user.save()
    timestamp = int(datetime.now().timestamp())

    # Act
    hash_value = generator._make_hash_value(user, timestamp)

    # Assert
    login_timestamp = user.last_login.replace(microsecond=0, tzinfo=None)
    expected_hash_value = f"{user.pk}{user.password}{login_timestamp}{timestamp}"
    
    assert hash_value == expected_hash_value

def test_make_hash_value_with_no_last_login(user):
    # Arrange
    generator = PasswordResetTokenGenerator()
    user.last_login = None
    user.save()
    timestamp = int(datetime.now().timestamp())

    # Act
    hash_value = generator._make_hash_value(user, timestamp)

    # Assert
    login_timestamp = ''  # No last_login means an empty string
    expected_hash_value = f"{user.pk}{user.password}{login_timestamp}{timestamp}"
    
    assert hash_value == expected_hash_value