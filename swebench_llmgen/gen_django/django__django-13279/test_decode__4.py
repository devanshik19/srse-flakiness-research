import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.core import signing
from django.core.exceptions import SuspiciousOperation

class TestSessionBase:
    def setup_method(self):
        self.session_base = SessionBase(session_key='test_key')

    def test_decode_valid_data(self):
        # Arrange
        session_data = signing.dumps({'key': 'value'}, salt=self.session_base.key_salt)
        
        # Act
        result = self.session_base.decode(session_data)
        
        # Assert
        assert result == {'key': 'value'}

    def test_decode_invalid_data(self):
        # Arrange
        session_data = "invalid_session_data"
        
        # Act / Assert
        with pytest.raises(SuspiciousOperation):
            self.session_base.decode(session_data)

    def test_decode_empty_data(self):
        # Arrange
        session_data = ''
        
        # Act / Assert
        with pytest.raises(SuspiciousOperation):
            self.session_base.decode(session_data)

    def test_decode_with_legacy_fallback(self, monkeypatch):
        # Arrange
        def mock_legacy_decode(self, session_data):
            return {'legacy_key': 'legacy_value'}
        
        monkeypatch.setattr(SessionBase, "_legacy_decode", mock_legacy_decode)
        session_data = "invalid_session_data"
        
        # Act
        result = self.session_base.decode(session_data)
        
        # Assert
        assert result == {'legacy_key': 'legacy_value'}