import pytest
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.db.backends.mysql.base import DatabaseWrapper

@pytest.fixture
def db_wrapper(settings):
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'isolation_level': 'read committed',
        }
    }
    return DatabaseWrapper(settings_dict=settings.DATABASES['default'])

def test_get_connection_params_with_all_params(db_wrapper):
    params = db_wrapper.get_connection_params()
    assert params['user'] == 'test_user'
    assert params['db'] == 'test_db'
    assert params['passwd'] == 'test_password'
    assert params['host'] == 'localhost'
    assert params['port'] == 3306
    assert params['client_flag'] == 0b10000  # CLIENT.FOUND_ROWS (actual value might differ based on implementation)

def test_get_connection_params_with_unix_socket(db_wrapper):
    db_wrapper.settings_dict['HOST'] = '/var/run/mysqld/mysqld.sock'
    params = db_wrapper.get_connection_params()
    assert 'unix_socket' in params
    assert params['unix_socket'] == '/var/run/mysqld/mysqld.sock'

def test_get_connection_params_without_credentials(db_wrapper):
    db_wrapper.settings_dict['USER'] = ''
    db_wrapper.settings_dict['PASSWORD'] = ''
    params = db_wrapper.get_connection_params()
    assert 'user' not in params
    assert 'passwd' not in params

def test_get_connection_params_invalid_isolation_level(db_wrapper):
    db_wrapper.settings_dict['OPTIONS']['isolation_level'] = 'invalid_level'
    with pytest.raises(ImproperlyConfigured):
        db_wrapper.get_connection_params()