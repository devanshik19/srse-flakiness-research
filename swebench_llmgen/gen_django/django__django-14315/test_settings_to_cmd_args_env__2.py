import pytest
from django.db.backends.postgresql.client import DatabaseClient

def test_settings_to_cmd_args_env():
    # Arrange
    DatabaseClient.executable_name = 'psql'
    settings_dict = {
        'HOST': 'localhost',
        'PORT': 5432,
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_password',
        'OPTIONS': {
            'passfile': '/path/to/passfile',
            'service': 'my_service',
            'sslmode': 'require',
            'sslrootcert': '/path/to/root.crt',
            'sslcert': '/path/to/cert.crt',
            'sslkey': '/path/to/key.key',
        }
    }
    parameters = ['--no-password']

    # Act
    args, env = DatabaseClient.settings_to_cmd_args_env(settings_dict, parameters)

    # Assert
    assert args == [
        'psql',
        '-U', 'test_user',
        '-h', 'localhost',
        '-p', '5432',
        'test_db',
        '--no-password'
    ]
    assert env == {
        'PGPASSWORD': 'test_password',
        'PGSERVICE': 'my_service',
        'PGSSLMODE': 'require',
        'PGSSLROOTCERT': '/path/to/root.crt',
        'PGSSLCERT': '/path/to/cert.crt',
        'PGSSLKEY': '/path/to/key.key',
        'PGPASSFILE': '/path/to/passfile',
    }

    # Test with missing dbname and service
    settings_dict_no_db = {
        'HOST': 'localhost',
        'PORT': 5432,
        'OPTIONS': {}
    }
    
    args_no_db, env_no_db = DatabaseClient.settings_to_cmd_args_env(settings_dict_no_db, parameters)
    assert args_no_db == [
        'psql',
        '-h', 'localhost',
        '-p', '5432',
        'postgres',
        '--no-password'
    ]
    assert env_no_db == {}