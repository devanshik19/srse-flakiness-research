import pytest
from django.core.exceptions import ImproperlyConfigured
from django.db.backends.mysql.base import DatabaseWrapper

@pytest.fixture
def db_wrapper():
    settings = {
        'USER': 'testuser',
        'NAME': 'testdb',
        'PASSWORD': 'testpass',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'isolation_level': 'read committed'}
    }
    wrapper = DatabaseWrapper(settings_dict=settings)
    return wrapper

def test_get_connection_params_with_valid_settings(db_wrapper):
    params = db_wrapper.get_connection_params()
    assert params['conv'] == db_wrapper.conversions
    assert params['charset'] == 'utf8'
    assert params['user'] == 'testuser'
    assert params['db'] == 'testdb'
    assert params['passwd'] == 'testpass'
    assert params['host'] == 'localhost'
    assert params['port'] == 3306
    assert params['client_flag'] == CLIENT.FOUND_ROWS
    assert db_wrapper.isolation_level == 'read committed'

def test_get_connection_params_with_unix_socket(db_wrapper):
    db_wrapper.settings_dict['HOST'] = '/var/run/mysql.sock'
    params = db_wrapper.get_connection_params()
    assert params['unix_socket'] == '/var/run/mysql.sock'

def test_get_connection_params_with_no_user(db_wrapper):
    db_wrapper.settings_dict['USER'] = ''
    params = db_wrapper.get_connection_params()
    assert 'user' not in params

def test_get_connection_params_with_no_db_name(db_wrapper):
    db_wrapper.settings_dict['NAME'] = ''
    params = db_wrapper.get_connection_params()
    assert 'db' not in params

def test_get_connection_params_with_invalid_isolation_level(db_wrapper):
    db_wrapper.settings_dict['OPTIONS']['isolation_level'] = 'invalid_level'
    with pytest.raises(ImproperlyConfigured):
        db_wrapper.get_connection_params()

def test_get_connection_params_with_default_isolation_level(db_wrapper):
    db_wrapper.settings_dict['OPTIONS']['isolation_level'] = None
    params = db_wrapper.get_connection_params()
    assert db_wrapper.isolation_level is None