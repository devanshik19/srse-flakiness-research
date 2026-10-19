import pytest
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.db.backends.mysql.base import DatabaseWrapper

@pytest.fixture
def db_wrapper(settings):
    # Configure the settings for the test
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_pass',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'isolation_level': 'read committed'
        }
    }
    return DatabaseWrapper(settings_dict=settings.DATABASES['default'])

def test_get_connection_params_user(db_wrapper):
    params = db_wrapper.get_connection_params()
    assert params['user'] == 'test_user'

def test_get_connection_params_db(db_wrapper):
    params = db_wrapper.get_connection_params()
    assert params['db'] == 'test_db'

def test_get_connection_params_password(db_wrapper):
    params = db_wrapper.get_connection_params()
    assert params['passwd'] == 'test_pass'

def test_get_connection_params_host(db_wrapper):
    params = db_wrapper.get_connection_params()
    assert params['host'] == 'localhost'

def test_get_connection_params_port(db_wrapper):
    params = db_wrapper.get_connection_params()
    assert params['port'] == 3306

def test_get_connection_params_unix_socket(db_wrapper):
    settings.DATABASES['default']['HOST'] = '/var/run/mysqld/mysqld.sock'
    db_wrapper = DatabaseWrapper(settings_dict=settings.DATABASES['default'])
    params = db_wrapper.get_connection_params()
    assert params['unix_socket'] == '/var/run/mysqld/mysqld.sock'

def test_get_connection_params_invalid_isolation_level(db_wrapper):
    settings.DATABASES['default']['OPTIONS']['isolation_level'] = 'invalid_level'
    db_wrapper = DatabaseWrapper(settings_dict=settings.DATABASES['default'])
    with pytest.raises(ImproperlyConfigured):
        db_wrapper.get_connection_params()

def test_get_connection_params_default_isolation_level(db_wrapper):
    settings.DATABASES['default']['OPTIONS'].pop('isolation_level', None)
    db_wrapper = DatabaseWrapper(settings_dict=settings.DATABASES['default'])
    params = db_wrapper.get_connection_params()
    assert db_wrapper.isolation_level == 'read committed'