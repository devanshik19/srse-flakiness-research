import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.utils.crypto import get_random_string

class TestSessionBase:

    @pytest.fixture
    def session_base(self):
        return SessionBase(session_key=get_random_string(10))

    def test_hash_valid_input(self, session_base):
        value = "test_value"
        expected_hash = session_base._hash(value)
        assert isinstance(expected_hash, str)
        assert len(expected_hash) > 0

    def test_hash_different_values(self, session_base):
        value1 = "test_value1"
        value2 = "test_value2"
        hash1 = session_base._hash(value1)
        hash2 = session_base._hash(value2)
        assert hash1 != hash2

    def test_hash_non_string_input(self, session_base):
        value = 12345
        with pytest.raises(TypeError):
            session_base._hash(value)