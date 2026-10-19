import pytest
from django.core.exceptions import ImproperlyConfigured
from django.db.backends.mysql.base import DatabaseWrapper

@pytest.fixture
def db_wrapper():
    settings = {
        'USER': 'test_user',
        'NAME': 'test_db',
        'PASSWORD': 'test_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'isolation_level': 'read committed'
        }
    }
    wrapper = DatabaseWrapper(settings_dict=settings)
    return wrapper

def test_get_connection_params_with_valid_settings(db_wrapper):
    expected_params = {
        'conv': db_wrapper.django_conversions,
        'charset': 'utf8',
        'user': 'test_user',
        'db': 'test_db',
        'passwd': 'test_password',
        'host': 'localhost',
        'port': 3306,
        'client_flag': 1,  # CLIENT.FOUND_ROWS
        'isolation_level': 'read committed',
    }
    assert db_wrapper.get_connection_params() == expected_params

def test_get_connection_params_with_unix_socket(db_wrapper):
    db_wrapper.settings_dict['HOST'] = '/var/run/mysqld/mysqld.sock'
    expected_params = {
        'conv': db_wrapper.django_conversions,
        'charset': 'utf8',
        'user': 'test_user',
        'db': 'test_db',
        'passwd': 'test_password',
        'unix_socket': '/var/run/mysqld/mysqld.sock',
        'client_flag': 1,  # CLIENT.FOUND_ROWS
        'isolation_level': 'read committed',
    }
    assert db_wrapper.get_connection_params() == expected_params

def test_get_connection_params_with_no_user(db_wrapper):
    db_wrapper.settings_dict['USER'] = ''
    db_wrapper.settings_dict['NAME'] = 'test_db'
    expected_params = {
        'conv': db_wrapper.django_conversions,
        'charset': 'utf8',
        'db': 'test_db',
        'client_flag': 1,  # CLIENT.FOUND_ROWS
        'isolation_level': 'read committed',
    }
    assert db_wrapper.get_connection_params() == expected_params

def test_get_connection_params_invalid_isolation_level(db_wrapper):
    db_wrapper.settings_dict['OPTIONS']['isolation_level'] = 'invalid_level'
    with pytest.raises(ImproperlyConfigured):
        db_wrapper.get_connection_params()