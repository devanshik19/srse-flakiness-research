import pytest
from django.core.exceptions import ImproperlyConfigured
from django.db.backends.mysql.base import DatabaseWrapper

@pytest.fixture
def db_wrapper():
    # Create a DatabaseWrapper instance with necessary settings.
    settings = {
        'USER': 'test_user',
        'NAME': 'test_db',
        'PASSWORD': 'test_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {}
    }
    wrapper = DatabaseWrapper(settings_dict=settings)
    return wrapper

def test_get_connection_params_with_required_fields(db_wrapper):
    params = db_wrapper.get_connection_params()
    assert params['conv'] is not None
    assert params['charset'] == 'utf8'
    assert params['user'] == 'test_user'
    assert params['db'] == 'test_db'
    assert params['passwd'] == 'test_password'
    assert params['host'] == '127.0.0.1'
    assert params['port'] == 3306
    assert params['client_flag'] == CLIENT.FOUND_ROWS

def test_get_connection_params_with_unix_socket(db_wrapper):
    db_wrapper.settings_dict['HOST'] = '/var/run/mysqld/mysqld.sock'
    params = db_wrapper.get_connection_params()
    assert 'unix_socket' in params
    assert params['unix_socket'] == '/var/run/mysqld/mysqld.sock'

def test_get_connection_params_without_optional_fields(db_wrapper):
    db_wrapper.settings_dict['USER'] = ''
    db_wrapper.settings_dict['NAME'] = ''
    db_wrapper.settings_dict['PASSWORD'] = ''
    db_wrapper.settings_dict['HOST'] = ''
    db_wrapper.settings_dict['PORT'] = ''
    params = db_wrapper.get_connection_params()
    assert 'user' not in params
    assert 'db' not in params
    assert 'passwd' not in params
    assert 'host' not in params
    assert 'port' not in params

def test_get_connection_params_with_invalid_isolation_level(db_wrapper):
    db_wrapper.settings_dict['OPTIONS']['isolation_level'] = 'invalid_level'
    with pytest.raises(ImproperlyConfigured):
        db_wrapper.get_connection_params()