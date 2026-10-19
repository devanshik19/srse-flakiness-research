import pytest
from django.core.exceptions import ImproperlyConfigured
from django.db.backends.mysql.base import DatabaseWrapper

@pytest.fixture
def db_wrapper(settings):
    settings.DATABASES = {
        'default': {
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
    }
    return DatabaseWrapper(settings_dict=settings.DATABASES['default'])

def test_get_connection_params_with_all_options(db_wrapper):
    expected_params = {
        'conv': db_wrapper.conversions,
        'charset': 'utf8',
        'user': 'test_user',
        'db': 'test_db',
        'passwd': 'test_pass',
        'host': 'localhost',
        'port': 3306,
        'client_flag': 0x00020000,  # CLIENT.FOUND_ROWS
        'isolation_level': 'read committed',
    }
    
    params = db_wrapper.get_connection_params()
    assert params == expected_params

def test_get_connection_params_with_socket(db_wrapper, settings):
    settings.DATABASES['default']['HOST'] = '/var/run/mysqld/mysqld.sock'
    expected_params = {
        'conv': db_wrapper.conversions,
        'charset': 'utf8',
        'user': 'test_user',
        'db': 'test_db',
        'passwd': 'test_pass',
        'unix_socket': '/var/run/mysqld/mysqld.sock',
        'client_flag': 0x00020000,  # CLIENT.FOUND_ROWS
        'isolation_level': 'read committed',
    }

    params = db_wrapper.get_connection_params()
    assert params == expected_params

def test_get_connection_params_invalid_isolation_level(db_wrapper):
    db_wrapper.settings_dict['OPTIONS']['isolation_level'] = 'invalid_level'
    with pytest.raises(ImproperlyConfigured) as excinfo:
        db_wrapper.get_connection_params()
    assert "Invalid transaction isolation level" in str(excinfo.value)

def test_get_connection_params_without_user(db_wrapper):
    db_wrapper.settings_dict['USER'] = ''
    expected_params = {
        'conv': db_wrapper.conversions,
        'charset': 'utf8',
        'db': 'test_db',
        'passwd': 'test_pass',
        'host': 'localhost',
        'port': 3306,
        'client_flag': 0x00020000,  # CLIENT.FOUND_ROWS
        'isolation_level': 'read committed',
    }

    params = db_wrapper.get_connection_params()
    assert 'user' not in params
    assert params == expected_params