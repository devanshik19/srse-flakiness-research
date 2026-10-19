import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.utils.crypto import get_random_string

class TestSessionBase:

    @pytest.fixture
    def session_base(self):
        return SessionBase(session_key=get_random_string(10))

    def test_hash(self, session_base):
        value = "test_value"
        expected_hash = session_base._hash(value)
        
        # Check that the hash is consistent
        assert expected_hash == session_base._hash(value)

        # Check that different values generate different hashes
        different_value = "different_value"
        assert expected_hash != session_base._hash(different_value)

        # Check that the hash has a correct length (hexdigest of SHA1 is 40 characters long)
        assert len(expected_hash) == 40