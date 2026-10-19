import pytest
from django.core.exceptions import ImproperlyConfigured
from django.db.backends.mysql.base import DatabaseWrapper

@pytest.fixture
def database_wrapper():
    settings_dict = {
        'USER': 'test_user',
        'NAME': 'test_db',
        'PASSWORD': 'test_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'isolation_level': 'read committed'},
    }
    db_wrapper = DatabaseWrapper()
    db_wrapper.settings_dict = settings_dict
    return db_wrapper

def test_get_connection_params_valid(database_wrapper):
    params = database_wrapper.get_connection_params()
    assert params['conv'] == database_wrapper.conversions  # Assuming django_conversions is set up properly
    assert params['charset'] == 'utf8'
    assert params['user'] == 'test_user'
    assert params['db'] == 'test_db'
    assert params['passwd'] == 'test_password'
    assert params['host'] == 'localhost'
    assert params['port'] == 3306
    assert params['client_flag'] == CLIENT.FOUND_ROWS
    assert database_wrapper.isolation_level == 'read committed'

def test_get_connection_params_unix_socket(database_wrapper):
    database_wrapper.settings_dict['HOST'] = '/var/run/mysqld/mysqld.sock'
    params = database_wrapper.get_connection_params()
    assert params['unix_socket'] == '/var/run/mysqld/mysqld.sock'

def test_get_connection_params_invalid_isolation_level(database_wrapper):
    database_wrapper.settings_dict['OPTIONS']['isolation_level'] = 'invalid_level'
    with pytest.raises(ImproperlyConfigured) as excinfo:
        database_wrapper.get_connection_params()
    assert "Invalid transaction isolation level" in str(excinfo.value)

def test_get_connection_params_no_user(database_wrapper):
    database_wrapper.settings_dict['USER'] = ''
    params = database_wrapper.get_connection_params()
    assert 'user' not in params

def test_get_connection_params_no_name(database_wrapper):
    database_wrapper.settings_dict['NAME'] = ''
    params = database_wrapper.get_connection_params()
    assert 'db' not in params

def test_get_connection_params_no_password(database_wrapper):
    database_wrapper.settings_dict['PASSWORD'] = ''
    params = database_wrapper.get_connection_params()
    assert 'passwd' not in params