import pytest
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime

@pytest.mark.django_db
def test_make_hash_value():
    generator = PasswordResetTokenGenerator()
    
    # Create a user instance
    user = User.objects.create_user(username='testuser', password='testpass')
    
    # Test with different timestamps
    timestamp1 = int(datetime.now().timestamp())
    hash_value1 = generator._make_hash_value(user, timestamp1)
    
    # Assert the hash value contains user.pk, user.password, and timestamp
    assert str(user.pk) in hash_value1
    assert user.password in hash_value1
    assert str(timestamp1) in hash_value1
    
    # Simulate a password change
    user.set_password('newpass')
    user.save()
    
    timestamp2 = int(datetime.now().timestamp())
    hash_value2 = generator._make_hash_value(user, timestamp2)
    
    # Assert the hash value has changed due to password change
    assert str(user.pk) in hash_value2
    assert 'testpass' not in hash_value2  # Ensure old password is not in new hash
    assert user.password in hash_value2
    assert str(timestamp2) in hash_value2
    
    # Simulate last_login
    user.last_login = datetime.now()
    user.save()

    hash_value3 = generator._make_hash_value(user, timestamp2)
    
    # Assert the login timestamp is now reflected in the hash
    assert str(user.pk) in hash_value3
    assert user.password in hash_value3
    assert str(timestamp2) in hash_value3
    
    # Ensure hash values are distinct across different user states
    assert hash_value1 != hash_value2
    assert hash_value2 != hash_value3