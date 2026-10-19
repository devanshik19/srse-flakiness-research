import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.utils.crypto import salted_hmac

class TestSessionBase:
    def setup_method(self):
        self.session = SessionBase(session_key='test_session_key')

    def test_hash(self):
        value = "test_value"
        key_salt = "django.contrib.sessionsSessionBase"
        expected_hash = salted_hmac(key_salt, value).hexdigest()
        
        # Test that _hash produces the expected hash
        actual_hash = self.session._hash(value)
        assert actual_hash == expected_hash

    def test_hash_empty_string(self):
        value = ""
        key_salt = "django.contrib.sessionsSessionBase"
        expected_hash = salted_hmac(key_salt, value).hexdigest()
        
        # Test that _hash with an empty string produces the expected hash
        actual_hash = self.session._hash(value)
        assert actual_hash == expected_hash

    def test_hash_non_ascii(self):
        value = "𝓣𝓮𝔁𝓽"  # Non-ASCII characters
        key_salt = "django.contrib.sessionsSessionBase"
        expected_hash = salted_hmac(key_salt, value).hexdigest()
        
        # Test that _hash with non-ASCII produces the expected hash
        actual_hash = self.session._hash(value)
        assert actual_hash == expected_hash