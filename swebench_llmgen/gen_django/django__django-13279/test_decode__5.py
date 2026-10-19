import base64
import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.core import signing
from django.contrib.auth.models import User
from django.core.exceptions import SuspiciousOperation

@pytest.fixture
def session_base():
    return SessionBase(session_key='test_session_key')

def test_decode_valid_data(session_base):
    # Simulate a valid encoded session
    session_dict = {'user_id': 1}
    session_data = signing.dumps(session_dict, salt=session_base.key_salt)

    decoded_data = session_base.decode(session_data)
    assert decoded_data['user_id'] == 1

def test_decode_invalid_data_legacy(session_base):
    # Simulate an invalid encoded session
    invalid_session_data = base64.b64encode(b'invalid_data').decode('utf-8')

    with pytest.raises(SuspiciousOperation):
        session_base.decode(invalid_session_data)

def test_decode_raises_exception(session_base):
    # Simulate raising an exception in signing.loads
    with pytest.raises(Exception):
        session_base.decode(None)

def test_decode_with_empty_string(session_base):
    # Test decoding an empty string
    decoded_data = session_base.decode('')
    assert decoded_data is None  # Should return None or similar for empty input