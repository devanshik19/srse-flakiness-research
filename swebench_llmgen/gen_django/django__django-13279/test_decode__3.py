import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.core import signing
from django.core.exceptions import SuspiciousOperation

class TestSessionBase:

    def test_decode_valid_session_data(self):
        session_data = signing.dumps({'user_id': 42})
        session_base = SessionBase("test")
        decoded_data = session_base.decode(session_data)
        assert decoded_data['user_id'] == 42

    def test_decode_invalid_session_data(self):
        session_base = SessionBase("test")
        with pytest.raises(SuspiciousOperation):
            session_base.decode("invalid_data")

    def test_decode_failure_falls_back_to_legacy_decode(self, monkeypatch):
        def legacy_decode_mock(session_data):
            return {'user_id': 0}  # Simulated fallback return data

        monkeypatch.setattr(SessionBase, '_legacy_decode', legacy_decode_mock)
        session_data = "invalid_data"
        session_base = SessionBase("test")
        decoded_data = session_base.decode(session_data)
        assert decoded_data['user_id'] == 0