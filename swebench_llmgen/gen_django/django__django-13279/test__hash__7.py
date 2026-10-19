import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.utils.crypto import get_random_string

class TestSessionBase:

    def setup_method(self):
        self.session_key = get_random_string()
        self.session = SessionBase(self.session_key)

    def test_hash_valid_input(self):
        value = "test_value"
        hashed_value = self.session._hash(value)
        assert hashed_value is not None
        assert isinstance(hashed_value, str)

    def test_hash_different_values(self):
        value1 = "test_value1"
        value2 = "test_value2"
        hashed_value1 = self.session._hash(value1)
        hashed_value2 = self.session._hash(value2)
        assert hashed_value1 != hashed_value2

    def test_hash_same_value(self):
        value = "test_value"
        hashed_value1 = self.session._hash(value)
        hashed_value2 = self.session._hash(value)
        assert hashed_value1 == hashed_value2