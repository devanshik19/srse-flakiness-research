import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.utils.crypto import get_random_string

class TestSessionBase:
    @pytest.fixture
    def session_base(self):
        return SessionBase(session_key=get_random_string(10))

    def test_hash(self, session_base):
        value = "test_value"
        hashed_value = session_base._hash(value)

        # Ensure the hash is a valid hexadecimal string
        assert isinstance(hashed_value, str)
        assert all(c in string.hexdigits for c in hashed_value)
        
        # Test consistency: hashing the same value should return the same hash
        assert hashed_value == session_base._hash(value)

        # Test that different values produce different hashes
        different_value = "another_value"
        different_hashed_value = session_base._hash(different_value)
        assert hashed_value != different_hashed_value

        # Test with empty value
        empty_hashed_value = session_base._hash("")
        assert empty_hashed_value != hashed_value
        
        # Test with special characters
        special_char_value = "!@#$%^&*()"
        special_hashed_value = session_base._hash(special_char_value)
        assert special_hashed_value != empty_hashed_value