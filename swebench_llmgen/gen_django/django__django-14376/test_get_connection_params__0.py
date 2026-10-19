import pytest
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.db.backends.mysql.base import DatabaseWrapper

@pytest.fixture
def db_wrapper_with_params():
    settings_dict = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_pass',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {}
    }
    db_wrapper = DatabaseWrapper(settings_dict)
    return db_wrapper

def test_get_connection_params_with_minimum_params(db_wrapper_with_params):
    db_wrapper = db_wrapper_with_params
    params = db_wrapper.get_connection_params()
    
    assert params['user'] == 'test_user'
    assert params['db'] == 'test_db'
    assert params['passwd'] == 'test_pass'
    assert params['host'] == 'localhost'
    assert params['port'] == 3306
    assert params['charset'] == 'utf8'
    assert params['client_flag'] == 32  # Assuming CLIENT.FOUND_ROWS is 32
    assert db_wrapper.isolation_level == 'read committed'

def test_get_connection_params_with_unix_socket(db_wrapper_with_params):
    db_wrapper = db_wrapper_with_params
    db_wrapper.settings_dict['HOST'] = '/var/run/mysqld/mysqld.sock'
    params = db_wrapper.get_connection_params()
    
    assert 'unix_socket' in params
    assert params['unix_socket'] == '/var/run/mysqld/mysqld.sock'

def test_get_connection_params_with_invalid_isolation_level(db_wrapper_with_params):
    db_wrapper = db_wrapper_with_params
    db_wrapper.settings_dict['OPTIONS'] = {'isolation_level': 'invalid_level'}
    
    with pytest.raises(ImproperlyConfigured):
        db_wrapper.get_connection_params()

def test_get_connection_params_with_additional_options(db_wrapper_with_params):
    db_wrapper = db_wrapper_with_params
    db_wrapper.settings_dict['OPTIONS'] = {'isolation_level': 'serializable', 'autocommit': True}
    params = db_wrapper.get_connection_params()
    
    assert params['autocommit'] is True
    assert db_wrapper.isolation_level == 'serializable'