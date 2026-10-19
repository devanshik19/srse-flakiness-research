import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.core import signing
from django.core.exceptions import SuspiciousOperation


class TestSessionBase:
    @pytest.fixture
    def session_base(self):
        return SessionBase(session_key='test_key')

    def test_decode_valid_data(self, session_base):
        valid_data = signing.dumps({'key': 'value'}, salt=session_base.key_salt)
        result = session_base.decode(valid_data)
        assert result == {'key': 'value'}

    def test_decode_invalid_data(self, session_base):
        invalid_data = b'invalid_data'
        result = session_base.decode(invalid_data)
        assert result == session_base._legacy_decode(invalid_data)

    def test_decode_suspicious_operation(self, session_base):
        with pytest.raises(SuspiciousOperation):
            session_base.decode(b'suspicious_data')