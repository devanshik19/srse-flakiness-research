import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.utils.crypto import get_random_string

class TestSessionBase:

    @pytest.fixture
    def session_base(self):
        return SessionBase(session_key=get_random_string(32))

    def test_hash_value(self, session_base):
        value = "test_value"
        expected_hash = session_base._hash(value)

        # Test the hash generation
        assert isinstance(expected_hash, str)
        assert expected_hash == session_base._hash(value)  # Same input should yield same hash

    def test_hash_different_values(self, session_base):
        value1 = "value1"
        value2 = "value2"
        
        # Test different values produce different hashes
        assert session_base._hash(value1) != session_base._hash(value2)

    def test_hash_randomness(self, session_base):
        # Checking randomness: multiple hashes for the same value should theoretically vary
        hashes = {session_base._hash("same_value") for _ in range(10)}
        assert len(hashes) == 1  # Same input should always yield the same hash

    def test_hash_is_not_empty(self, session_base):
        value = "some_value"
        result = session_base._hash(value)
        assert result != ""