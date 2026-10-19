import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.core import signing
from django.core.exceptions import SuspiciousOperation
from django.utils import timezone
import base64


class TestSessionBase:
    def setup_method(self):
        self.session = SessionBase(session_key="test_session_key")
        self.session.key_salt = "test_salt"
        self.session.serializer = signing.JSONSerializer()

    def test_decode_valid_data(self):
        # Prepare valid data for encoding and decoding
        valid_data = {"user_id": 1, "last_activity": timezone.now().isoformat()}
        encoded_data = signing.dumps(valid_data, salt=self.session.key_salt, serializer=self.session.serializer)
        
        decoded_data = self.session.decode(encoded_data)
        assert decoded_data == valid_data

    def test_decode_invalid_data(self):
        # Attempt decoding invalid data
        with pytest.raises(SuspiciousOperation):
            self.session.decode("invalid_session_data")

    def test_decode_legacy_fallback(self, monkeypatch):
        # Test legacy decode if signing.loads raises an exception
        monkeypatch.setattr(signing, 'loads', lambda x, salt: (_ for _ in ()).throw(SuspiciousOperation))
        self.session._legacy_decode = lambda x: {"legacy": "fallback"}

        result = self.session.decode("any_invalid_data")
        assert result == {"legacy": "fallback"}