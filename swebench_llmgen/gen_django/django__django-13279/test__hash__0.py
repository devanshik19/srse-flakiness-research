import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.utils.crypto import get_random_string

class TestSessionBase:

    def setup_method(self):
        self.session = SessionBase(session_key="test_key")

    def test_hash(self):
        # Test that _hash returns a valid hash
        test_value = get_random_string(32)
        hash_value = self.session._hash(test_value)
        
        # Verify that the hash is not None
        assert hash_value is not None
        
        # Verify that hashing the same value returns the same hash
        assert hash_value == self.session._hash(test_value)
        
        # Check that hashing a different value returns a different hash
        other_value = get_random_string(32)
        assert hash_value != self.session._hash(other_value)

        # Check that key_salt as part of the hash is correctly tied to this session type
        assert "django.contrib.sessionsSessionBase" in hash_value