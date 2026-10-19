import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.core import signing
from django.core.exceptions import SuspiciousOperation

class TestSessionBase:
    def setup_method(self):
        self.session = SessionBase(session_key='test_key')
        self.valid_session_data = signing.dumps({'key': 'value'}, salt=self.session.key_salt)
        self.invalid_session_data = 'invalid_session_data'

    def test_decode_valid_data(self):
        result = self.session.decode(self.valid_session_data)
        assert isinstance(result, dict)
        assert result['key'] == 'value'

    def test_decode_invalid_data(self):
        with pytest.raises(SuspiciousOperation):
            self.session.decode(self.invalid_session_data)

    def test_decode_legacy_handling(self):
        # Simulating the legacy decode with improper format
        legacy_data = signing.dumps({'key': 'value'}, salt=self.session.key_salt).encode('utf-8')

        def legacy_decode_override(session_data):
            return {'legacy_key': 'legacy_value'}

        self.session._legacy_decode = legacy_decode_override
        result = self.session.decode(legacy_data)
        assert isinstance(result, dict)
        assert result['legacy_key'] == 'legacy_value'

    def test_decode_raises_exception(self):
        with pytest.raises(Exception):
            self.session.decode(None)