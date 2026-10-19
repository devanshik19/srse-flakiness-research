import pytest
from django.core.exceptions import ImproperlyConfigured
from django.db.backends.mysql.base import DatabaseWrapper

def test_get_connection_params_with_all_settings():
    db_wrapper = DatabaseWrapper()
    db_wrapper.settings_dict = {
        'USER': 'test_user',
        'NAME': 'test_db',
        'PASSWORD': 'test_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {}
    }

    expected_params = {
        'conv': db_wrapper.conversions,
        'charset': 'utf8',
        'user': 'test_user',
        'db': 'test_db',
        'passwd': 'test_password',
        'host': 'localhost',
        'port': 3306,
        'client_flag': db_wrapper.CLIENT.FOUND_ROWS,
        'isolation_level': 'read committed'
    }
    
    assert db_wrapper.get_connection_params() == expected_params

def test_get_connection_params_with_unix_socket():
    db_wrapper = DatabaseWrapper()
    db_wrapper.settings_dict = {
        'USER': 'test_user',
        'NAME': 'test_db',
        'PASSWORD': 'test_password',
        'HOST': '/tmp/mysql.sock',
        'PORT': '',
        'OPTIONS': {}
    }

    expected_params = {
        'conv': db_wrapper.conversions,
        'charset': 'utf8',
        'user': 'test_user',
        'db': 'test_db',
        'passwd': 'test_password',
        'unix_socket': '/tmp/mysql.sock',
        'client_flag': db_wrapper.CLIENT.FOUND_ROWS,
        'isolation_level': 'read committed'
    }
    
    assert db_wrapper.get_connection_params() == expected_params

def test_get_connection_params_with_invalid_isolation_level():
    db_wrapper = DatabaseWrapper()
    db_wrapper.settings_dict = {
        'USER': 'test_user',
        'NAME': 'test_db',
        'PASSWORD': 'test_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'isolation_level': 'invalid_level'}
    }

    with pytest.raises(ImproperlyConfigured, match="Invalid transaction isolation level 'invalid_level' specified."):
        db_wrapper.get_connection_params()

def test_get_connection_params_with_no_settings():
    db_wrapper = DatabaseWrapper()
    db_wrapper.settings_dict = {
        'USER': '',
        'NAME': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {}
    }

    expected_params = {
        'conv': db_wrapper.conversions,
        'charset': 'utf8',
        'client_flag': db_wrapper.CLIENT.FOUND_ROWS,
        'isolation_level': 'read committed'
    }
    
    assert db_wrapper.get_connection_params() == expected_params