import pytest
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.db.backends.mysql.base import DatabaseWrapper

def test_get_connection_params_with_user_and_name():
    db_wrapper = DatabaseWrapper()
    db_wrapper.settings_dict = {
        'USER': 'test_user',
        'NAME': 'test_db',
        'PASSWORD': 'test_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {}
    }
    
    params = db_wrapper.get_connection_params()
    
    assert params['user'] == 'test_user'
    assert params['db'] == 'test_db'
    assert 'passwd' in params
    assert 'host' in params
    assert params['port'] == 3306
    assert params['charset'] == 'utf8'
    assert params['client_flag'] == CLIENT.FOUND_ROWS

def test_get_connection_params_with_unix_socket():
    db_wrapper = DatabaseWrapper()
    db_wrapper.settings_dict = {
        'USER': 'test_user',
        'NAME': 'test_db',
        'PASSWORD': 'test_password',
        'HOST': '/var/run/mysqld/mysqld.sock',
        'PORT': '',
        'OPTIONS': {}
    }
    
    params = db_wrapper.get_connection_params()
    
    assert params['unix_socket'] == '/var/run/mysqld/mysqld.sock'
    assert params['user'] == 'test_user'
    assert params['db'] == 'test_db'
    assert 'passwd' in params

def test_get_connection_params_with_isolation_level():
    db_wrapper = DatabaseWrapper()
    db_wrapper.settings_dict = {
        'USER': 'test_user',
        'NAME': 'test_db',
        'PASSWORD': 'test_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'isolation_level': 'read committed'}
    }
    
    params = db_wrapper.get_connection_params()
    
    assert db_wrapper.isolation_level == 'read committed'

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
    
    with pytest.raises(ImproperlyConfigured):
        db_wrapper.get_connection_params()