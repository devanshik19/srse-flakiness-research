import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.core import signing
from django.contrib.auth.models import User

class TestSessionBase:
    def setup_method(self):
        self.session = SessionBase(session_key='test_key')
        self.valid_session_data = signing.dumps({'user_id': 1})  # valid session data
        self.invalid_session_data = 'invalid_session_data'  # invalid session data

    def test_decode_valid_data(self):
        result = self.session.decode(self.valid_session_data)
        assert result['user_id'] == 1

    def test_decode_invalid_data_legacy_fallback(self):
        result = self.session.decode(self.invalid_session_data)
        # Assuming _legacy_decode will return None or raise an exception,
        # we can assert based on its expected outcome. Here we assert None.
        # As we cannot access _legacy_decode directly, assume its intended operation.
        expected = self.session._legacy_decode(self.invalid_session_data)
        assert result == expected