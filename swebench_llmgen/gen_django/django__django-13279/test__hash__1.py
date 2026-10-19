import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.utils.crypto import get_random_string

class TestSessionBase:
    def setup_method(self):
        self.session = SessionBase(session_key=get_random_string(32))

    def test_hash_with_valid_value(self):
        value = "test_value"
        expected_hash = self.session._hash(value)
        assert expected_hash == self.session._hash(value)

    def test_hash_with_different_values(self):
        value1 = "test_value1"
        value2 = "test_value2"
        hash1 = self.session._hash(value1)
        hash2 = self.session._hash(value2)
        assert hash1 != hash2

    def test_hash_with_none_value(self):
        with pytest.raises(TypeError):
            self.session._hash(None)

    def test_hash_with_empty_string(self):
        value = ""
        expected_hash = self.session._hash(value)
        assert expected_hash == self.session._hash(value)

    def test_hash_with_spaces(self):
        value = "   "
        expected_hash = self.session._hash(value)
        assert expected_hash == self.session._hash(value)

    def test_hash_is_consistent_for_same_input(self):
        value = "consistent_input"
        hash1 = self.session._hash(value)
        hash2 = self.session._hash(value)
        assert hash1 == hash2