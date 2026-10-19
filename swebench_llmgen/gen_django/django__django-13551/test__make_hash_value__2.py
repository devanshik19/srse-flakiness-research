import pytest
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime, timedelta

class TestPasswordResetTokenGenerator:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='testpassword')

    @pytest.fixture
    def token_generator(self):
        return PasswordResetTokenGenerator()

    def test_make_hash_value_with_login(self, user, token_generator):
        user.last_login = datetime.now()
        timestamp = int(datetime.now().timestamp())
        hash_value = token_generator._make_hash_value(user, timestamp)
        
        expected_value = f"{user.pk}{user.password}{user.last_login.replace(microsecond=0, tzinfo=None)}{timestamp}"
        assert hash_value == expected_value

    def test_make_hash_value_without_login(self, user, token_generator):
        user.last_login = None
        timestamp = int(datetime.now().timestamp())
        hash_value = token_generator._make_hash_value(user, timestamp)
        
        expected_value = f"{user.pk}{user.password}{''}{timestamp}"
        assert hash_value == expected_value

    def test_make_hash_value_with_different_timestamp(self, user, token_generator):
        user.last_login = datetime.now()
        timestamp = int(datetime.now().timestamp())
        hash_value1 = token_generator._make_hash_value(user, timestamp)
        
        # Simulate a different timestamp
        timestamp2 = int((datetime.now() + timedelta(seconds=1)).timestamp())
        hash_value2 = token_generator._make_hash_value(user, timestamp2)
        
        assert hash_value1 != hash_value2
        
    def test_make_hash_value_with_same_user_and_password(self, user, token_generator):
        user.last_login = datetime.now()
        timestamp1 = int(datetime.now().timestamp())
        hash_value1 = token_generator._make_hash_value(user, timestamp1)
        
        timestamp2 = int(datetime.now().timestamp())
        hash_value2 = token_generator._make_hash_value(user, timestamp2)
        
        assert hash_value1 != hash_value2